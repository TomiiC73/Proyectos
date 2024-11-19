package com.example.repositorios;

import com.example.entidades.Vino;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface VinoRepository extends JpaRepository<Vino, Long> {

    List<Vino> findAll();
}