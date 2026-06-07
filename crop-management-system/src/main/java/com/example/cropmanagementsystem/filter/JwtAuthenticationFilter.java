package com.example.cropmanagementsystem.filter;

import com.example.cropmanagementsystem.pojo.Users;
import com.example.cropmanagementsystem.mapper.UserMapper;
import com.example.cropmanagementsystem.util.JwtUtil;
import io.jsonwebtoken.Claims;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * JWT认证过滤器（完全适配你现有项目，无UserDetailsService）
 * 核心逻辑：拦截请求 → 提取Token → 验证Token → 查数据库获取用户 → 封装认证信息 → 存入Security上下文
 */
@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    // 注入你项目已有的JWT工具类
    @Autowired
    private JwtUtil jwtUtil;

    // 注入你项目已有的UserMapper，直接查数据库获取用户
    @Autowired
    private UserMapper userMapper;

    @Override
    protected void doFilterInternal(
            HttpServletRequest request,
            HttpServletResponse response,
            FilterChain filterChain
    ) throws ServletException, IOException {

        // 1. 从请求头提取Token（标准格式：Authorization: Bearer <token>）
        String token = getTokenFromRequest(request);
        // 无Token直接放行，交给SecurityConfig的规则处理
        if (!StringUtils.hasText(token)) {
            filterChain.doFilter(request, response);
            return;
        }

        // 2. 验证Token有效性（调用你自己的JwtUtil方法）
        if (!jwtUtil.validateToken(token)) {
            filterChain.doFilter(request, response);
            return;
        }

        // 3. 解析Token，获取用户名（你JwtUtil里存的subject就是用户名）
        Claims claims = jwtUtil.parseToken(token);
        String username = claims.getSubject();

        // 4. 用户名不为空，且Security上下文未认证时，执行认证逻辑
        if (StringUtils.hasText(username) && SecurityContextHolder.getContext().getAuthentication() == null) {
            // 直接用你的UserMapper查数据库，获取用户信息（完全用你自己的Users实体）
            Users user = userMapper.selectByUsername(username);

            // 用户存在，封装Spring Security需要的认证对象
            if (user != null) {
                // 构造权限列表（如果你的用户有角色，比如"ROLE_USER"，可以在这里加）
                List<GrantedAuthority> authorities = new ArrayList<>();
                // 示例：给普通用户加默认权限，有角色需求直接改这里
                authorities.add(new SimpleGrantedAuthority("ROLE_USER"));

                // 核心：创建Spring Security识别的认证Token
                // 第一个参数：用户主体（直接用你的Users对象，后续接口可直接获取）
                // 第二个参数：凭证（JWT模式下为null，不用密码）
                // 第三个参数：用户权限
                UsernamePasswordAuthenticationToken authToken =
                        new UsernamePasswordAuthenticationToken(user, null, authorities);

                // 绑定请求详情（IP、Session等，Security标准要求）
                authToken.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));

                // 把认证信息存入Security上下文，后续接口就能通过Security获取用户
                SecurityContextHolder.getContext().setAuthentication(authToken);
            }
        }

        // 5. 放行请求，进入后续Controller
        filterChain.doFilter(request, response);
    }

    /**
     * 从请求头提取Token
     */
    private String getTokenFromRequest(HttpServletRequest request) {
        String authHeader = request.getHeader("Authorization");
        if (StringUtils.hasText(authHeader) && authHeader.startsWith("Bearer ")) {
            // 截取"Bearer "后的Token部分，长度7
            return authHeader.substring(7);
        }
        return null;
    }
}