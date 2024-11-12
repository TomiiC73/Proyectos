package ar.edu.utn.frc.backend.repositorios;

import ar.edu.utn.frc.backend.entities.Interesado;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface InteresadoRepositorio extends JpaRepository<Interesado, Long> {

    Optional<Interesado> findById(Long id);

    @Query("SELECT i FROM Interesado i WHERE i.id = :id")
    Optional<Interesado> findInteresadoByPruebaId(Long id);
}