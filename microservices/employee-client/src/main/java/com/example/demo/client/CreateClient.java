package com.example.demo.client;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

import com.example.demo.dto.Employee;

@FeignClient(name = "ms-create")
public interface CreateClient {

    @PostMapping("/employees")
    Employee createEmployee(@RequestBody Employee employee);
}
