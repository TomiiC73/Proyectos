package ar.edu.utn.frc.backend.repositorios;

import ar.edu.utn.frc.backend.entities.Empleado;
import ar.edu.utn.frc.backend.entities.Prueba;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface PruebaRepositorio extends JpaRepository<Prueba, Long> {

    Optional<Prueba> findById(Long id);

    List<Prueba> findAll();

    List<Prueba> findByFechaHoraFinIsNull();

    List<Prueba> findByVehiculoId(Long vehiculoId);

    @Query("SELECT p FROM Prueba p WHERE p.vehiculo.id = :vehiculoId AND p.fechaHoraFin IS NULL")
    Optional<Prueba> findPruebaByVehiculoIdAndFechaHoraFinIsNull(@Param("vehiculoId") Long vehiculoId);

    @Query("SELECT p.empleado.legajo FROM Prueba p WHERE p.vehiculo.id = :id")
    Long findEmpleadoIdByVehiculoId(Long id);

    @Query("SELECT p.empleado FROM Prueba p WHERE p.id = :id")
    Optional<Empleado> findEmpleadoByPruebaId(Long id);
}