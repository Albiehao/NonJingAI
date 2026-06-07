package com.example.cropmanagementsystem.config;

import com.example.cropmanagementsystem.filter.JwtAuthenticationFilter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    // 注入我们写好的JWT过滤器
    @Autowired
    private JwtAuthenticationFilter jwtAuthenticationFilter;

    /**
     * 核心安全配置链
     */
    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
                // 启用CORS（允许前端跨域访问）
                .cors(cors -> {})
                // 关闭CSRF（JWT无状态，不需要）
                .csrf(csrf -> csrf.disable())
                // 设置会话管理为无状态（JWT不使用Session）
                .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
                // 配置请求权限规则
                .authorizeHttpRequests(auth -> auth
                        // 放行登录、注册接口（不需要认证）
                        .requestMatchers("/user/**").permitAll()
                        // 放行静态资源（头像图片）
                        .requestMatchers("/uploads/**").permitAll()
                        // 放行健康检查端点
                        .requestMatchers("/actuator/**").permitAll()
                        // 放行商品相关接口（分类、商品查询、农作物、用户-农作物关联、AI聊天）
                        .requestMatchers("/categories/**", "/agrochemicals/**", "/crops/**", "/userCrops/**", "/chat/**").permitAll()
                        // 放行文件上传
                        .requestMatchers("/file/**").permitAll()
                        // 其他所有接口都需要认证
                        .anyRequest().authenticated()
                )
                // 把我们的JWT过滤器，放在UsernamePasswordAuthenticationFilter之前执行
                .addFilterBefore(jwtAuthenticationFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    /**
     * 密码编码器（必须，登录时用BCrypt加密验证密码）
     */
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    /**
     * 认证管理器（登录接口需要用这个来做密码校验）
     */
    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration config) throws Exception {
        return config.getAuthenticationManager();
    }

    /**
     * CORS 配置：允许前端（Vite 开发服务器和 nginx）跨域访问
     */
    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration configuration = new CorsConfiguration();
        configuration.addAllowedOriginPattern("*");
        configuration.addAllowedMethod("*");
        configuration.addAllowedHeader("*");
        configuration.setAllowCredentials(true);
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }
}