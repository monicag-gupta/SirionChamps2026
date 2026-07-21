package com.example.demo.client;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;

import com.example.demo.dto.Employee;

@FeignClient(name = "ms-update")
public interface UpdateClient {

    @PutMapping("/employees/{id}")
    Employee updateEmployee(@PathVariable("id") Long id, @RequestBody Employee employee);
}
