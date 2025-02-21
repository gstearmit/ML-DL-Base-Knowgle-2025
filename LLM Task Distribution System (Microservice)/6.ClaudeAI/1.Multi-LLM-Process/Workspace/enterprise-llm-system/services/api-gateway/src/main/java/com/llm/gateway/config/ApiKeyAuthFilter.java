package com.llm.gateway.config;

import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.security.web.authentication.WebAuthenticationFilter;

import java.io.IOException;

public class ApiKeyAuthFilter extends WebAuthenticationFilter {

    private static final String API_KEY_HEADER = "x-api-key";
    private static final String API_KEY_VALUE = "enterprise_llm_actual_api_key"; // Thay thế bằng API key thực tế của bạn

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain)
            throws ServletException, IOException {
        String apiKey = request.getHeader(API_KEY_HEADER);
        if (API_KEY_VALUE.equals(apiKey)) {
            // Nếu API key hợp lệ, cho phép yêu cầu tiếp tục
            chain.doFilter(request, response);
        } else {
            // Nếu không hợp lệ, trả về lỗi 401
            response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "No API key found in request");
        }
    }
} 