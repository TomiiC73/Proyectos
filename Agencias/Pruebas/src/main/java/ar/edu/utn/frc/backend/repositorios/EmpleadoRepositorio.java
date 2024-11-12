package ar.edu.utn.frc.backend.repositorios;

import ar.edu.utn.frc.backend.entities.Empleado;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface EmpleadoRepositorio extends JpaRepository<Empleado, Long> {

    Optional<Empleado> findById(Long id);

    @Query("SELECT e.telefono FROM Empleado e")
    List<String> findTelefonos();

    @Query("SELECT e.telefono FROM Empleado e WHERE e.legajo = :legajo")
    String findTelefonoByLegajo(Long legajo);
}