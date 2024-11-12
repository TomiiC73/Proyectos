package ar.edu.utn.frc.backend.repositorios;

import ar.edu.utn.frc.backend.entities.Posicion;
import ar.edu.utn.frc.backend.entities.Vehiculo;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface VehiculoRepositorio extends JpaRepository<Vehiculo, Long> {

    Optional<Vehiculo> findById(Long id);

    @Query("SELECT v.id FROM Vehiculo v WHERE v.patente = :patente")
    Long findIdByPatente(String patente);

    Vehiculo findByPatente(String patente);

    @Query("SELECT v.patente FROM Vehiculo v WHERE v.id = :id")
    String findVehiculoPatenteById(Long id);
}