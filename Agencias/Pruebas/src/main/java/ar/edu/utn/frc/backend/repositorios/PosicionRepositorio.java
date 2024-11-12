package ar.edu.utn.frc.backend.repositorios;

import ar.edu.utn.frc.backend.entities.Posicion;
import ar.edu.utn.frc.backend.entities.Vehiculo;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

public interface PosicionRepositorio extends JpaRepository<Posicion, Long> {

    @Query("SELECT p.id FROM Posicion p WHERE p.vehiculo.id = :vehiculoId")
    Long findPosicionIdByVehiculoId(Long vehiculoId);

    Posicion findPosicionByVehiculoId(Long id);

    // Metodo para obtener la última posición del vehículo
    @Query("SELECT p FROM Posicion p WHERE p.vehiculo = :vehiculo ORDER BY p.fechaHora DESC LIMIT 1")
    Posicion findFirstByVehiculoOrderByFechaHoraDesc(@Param("vehiculo") Optional<Vehiculo> vehiculo);

    @Query("SELECT p FROM Posicion p WHERE p.vehiculo = :vehiculo")
    List<Posicion> findPosicionsByVehiculo(Optional<Vehiculo> vehiculo);

    @Query("SELECT p FROM Posicion p WHERE p.vehiculo = :vehiculo AND p.fechaHora BETWEEN :fechaHoraDesde AND :fechaHoraHasta")
    List<Posicion> findPosicionsByVehiculoAndFecha(@Param("vehiculo") Vehiculo vehiculo,
                                                   @Param("fechaHoraDesde") String fechaHoraDesde,
                                                   @Param("fechaHoraHasta") String fechaHoraHasta);
}