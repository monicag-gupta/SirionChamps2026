package com.demo.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.demo.entity.Skill;

public interface SkillRepository extends JpaRepository<Skill, Long> {

    List<Skill> findBySName(String sName);

}