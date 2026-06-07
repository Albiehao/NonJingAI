package com.example.cropmanagementsystem.service.impl;

import com.example.cropmanagementsystem.service.AiAssistantService;
import com.example.cropmanagementsystem.service.AiStreamingAssistantService;
import com.example.cropmanagementsystem.tools.AgrochemicalTools;
import com.example.cropmanagementsystem.tools.CropTools;
import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.chat.StreamingChatLanguageModel;
import dev.langchain4j.service.AiServices;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * AI Assistant 服务实现
 * 使用 LangChain4j AiServices 构建智能客服
 */
@Configuration
public class AiAssistantServiceImpl {

    @Autowired
    private ChatLanguageModel chatLanguageModel;

    @Autowired
    private StreamingChatLanguageModel streamingChatLanguageModel;

    @Autowired
    private AgrochemicalTools agrochemicalTools;

    @Autowired
    private CropTools cropTools;

    /**
     构建 AiAssistantService Bean（非流式）
     */
    @Bean
    public AiAssistantService aiAssistantService() {
        return AiServices.builder(AiAssistantService.class)
                .chatLanguageModel(chatLanguageModel)
                .tools(agrochemicalTools, cropTools)
                .build();
    }

    /**
     构建 AiStreamingAssistantService Bean（流式）
     */
    @Bean
    public AiStreamingAssistantService aiStreamingAssistantService() {
        return AiServices.builder(AiStreamingAssistantService.class)
                .streamingChatLanguageModel(streamingChatLanguageModel)
                .tools(agrochemicalTools, cropTools)
                .build();
    }

}