package ar.edu.utn.frc.backend.repositories;

import ar.edu.utn.frc.backend.entities.Notificacion;
import org.springframework.data.repository.CrudRepository;
import java.util.List;
import java.util.Optional;


public interface NotificacionRepositorio extends CrudRepository<Notificacion, Long> {

    Optional<Notificacion> findById(Long id);

    List<Notificacion> findAll();

}