package com.demo.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.demo.entity.Project;

public interface ProjectRepository extends JpaRepository<Project, Long> {

    List<Project> findByPmngr(String pmngr);

    List<Project> findByLanguage(String language);

}