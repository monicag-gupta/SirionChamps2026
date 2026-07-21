package com.demo.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.demo.entity.Team;

public interface TeamRepository extends JpaRepository<Team, Long> {

    List<Team> findByProjectPid(Long pid);

    List<Team> findByEmployeeEid(Long eid);

}