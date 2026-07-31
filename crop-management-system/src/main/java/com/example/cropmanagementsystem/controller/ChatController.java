package com.example.cropmanagementsystem.controller;

import com.example.cropmanagementsystem.pojo.Agrochemicals;
import com.example.cropmanagementsystem.pojo.ChatRequest;
import com.example.cropmanagementsystem.pojo.ChatResponse;
import com.example.cropmanagementsystem.pojo.ProductRecommendation;
import com.example.cropmanagementsystem.pojo.Result;
import com.example.cropmanagementsystem.service.AgrochemicalsService;
import com.example.cropmanagementsystem.service.AiAssistantService;
import com.example.cropmanagementsystem.service.AiStreamingAssistantService;
import dev.langchain4j.service.TokenStream;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@RestController
@RequestMapping("/chat")
public class ChatController {

    @Autowired
    private AiAssistantService aiAssistantService;

    @Autowired
    private AiStreamingAssistantService aiStreamingAssistantService;

    @Autowired
    private AgrochemicalsService agrochemicalsService;

    @PostMapping
    public Result<ChatResponse> chat(@RequestBody ChatRequest request) {
        if (request.getMessage() == null || request.getMessage().trim().isEmpty()) {
            return Result.error("消息不能为空");
        }

        try {
            String reply = aiAssistantService.chat(request.getMessage());
            List<ProductRecommendation> recommendations = extractRecommendations(reply);
            ChatResponse response = new ChatResponse(reply, recommendations);
            return Result.success(response);
        } catch (Exception e) {
            e.printStackTrace();
            return Result.error("AI 服务暂时不可用，请稍后再试");
        }
    }

    @PostMapping(value = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public SseEmitter chatStream(@RequestBody ChatRequest request) throws IOException {
        if (request.getMessage() == null || request.getMessage().trim().isEmpty()) {
            SseEmitter emitter = new SseEmitter();
            emitter.send(SseEmitter.event().name("error").data("消息不能为空"));
            emitter.send(SseEmitter.event().name("done").data(""));
            emitter.complete();
            return emitter;
        }

        SseEmitter emitter = new SseEmitter(120000L);
        AtomicBoolean closed = new AtomicBoolean(false);
        StringBuilder fullReply = new StringBuilder();

        emitter.onCompletion(() -> closed.set(true));
        emitter.onTimeout(() -> sendDoneAndComplete(emitter, closed, "流式响应超时，请重试"));
        emitter.onError(e -> sendDoneAndComplete(emitter, closed, "流式响应中断，请重试"));

        try {
            TokenStream tokenStream = aiStreamingAssistantService.chatStream(request.getMessage());
            tokenStream
                    .onNext(token -> {
                        if (closed.get()) {
                            return;
                        }
                        fullReply.append(token);
                        safeSend(emitter, closed, "token", token);
                    })
                    .onComplete(ignored -> {
                        if (closed.get()) {
                            return;
                        }
                        List<ProductRecommendation> recommendations = extractRecommendations(fullReply.toString());
                        safeSend(emitter, closed, "recommendations", recommendations);
                        sendDoneAndComplete(emitter, closed, null);
                    })
                    .onError(error -> sendDoneAndComplete(
                            emitter,
                            closed,
                            "AI 服务异常: " + (error == null ? "unknown error" : error.getMessage())
                    ))
                    .start();
        } catch (Exception e) {
            sendDoneAndComplete(emitter, closed, "服务异常: " + e.getMessage());
        }

        return emitter;
    }

    private List<ProductRecommendation> extractRecommendations(String reply) {
        List<ProductRecommendation> recommendations = new ArrayList<>();
        Pattern pattern = Pattern.compile("/products/(\\d+)|ID:\\s*(\\d+)|\\(ID:\\s*(\\d+)\\)");
        Matcher matcher = pattern.matcher(reply);

        while (matcher.find()) {
            String idStr = matcher.group(1) != null ? matcher.group(1) :
                    (matcher.group(2) != null ? matcher.group(2) : matcher.group(3));
            if (idStr != null) {
                try {
                    Long productId = Long.parseLong(idStr.trim());
                    boolean exists = recommendations.stream()
                            .anyMatch(r -> r.getProductId().equals(productId));
                    if (!exists) {
                        Agrochemicals product = agrochemicalsService.getById(productId);
                        if (product != null) {
                            recommendations.add(new ProductRecommendation(
                                    product.getId(),
                                    product.getProductName(),
                                    "/products/" + product.getId(),
                                    product.getMainImage(),
                                    product.getPrice() != null ? product.getPrice().toString() : null
                            ));
                        }
                    }
                } catch (NumberFormatException ignored) {
                    // ignore invalid product id
                }
            }
        }

        return recommendations;
    }

    private void safeSend(SseEmitter emitter, AtomicBoolean closed, String eventName, Object data) {
        if (closed.get()) {
            return;
        }
        try {
            emitter.send(SseEmitter.event().name(eventName).data(data));
        } catch (IOException e) {
            sendDoneAndComplete(emitter, closed, "连接已断开");
        }
    }

    private void sendDoneAndComplete(SseEmitter emitter, AtomicBoolean closed, String errorMessage) {
        if (!closed.compareAndSet(false, true)) {
            return;
        }
        try {
            if (errorMessage != null && !errorMessage.isBlank()) {
                emitter.send(SseEmitter.event().name("error").data(errorMessage));
            }
            emitter.send(SseEmitter.event().name("done").data(""));
            emitter.complete();
        } catch (IOException e) {
            emitter.completeWithError(e);
        }
    }
}
