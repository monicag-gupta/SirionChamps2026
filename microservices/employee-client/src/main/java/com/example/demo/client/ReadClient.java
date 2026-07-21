package com.example.demo.client;

import java.util.List;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

import com.example.demo.dto.Employee;

@FeignClient(name = "ms-read")
public interface ReadClient {

    @GetMapping("/employees")
    List<Employee> getAllEmployees();

    @GetMapping("/employees/{id}")
    Employee getEmployeeById(@PathVariable("id") Long id);
}
