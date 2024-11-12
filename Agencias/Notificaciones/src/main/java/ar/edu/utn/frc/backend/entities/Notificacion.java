package ar.edu.utn.frc.backend.entities;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "Notificaciones")

public class Notificacion {
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "notificacion_generator")
    @SequenceGenerator(name = "notificacion_generator", sequenceName = "notificaciones_seq", allocationSize = 1)
    private Long id;

    @Column(name = "MENSAJE", nullable = false)
    private String mensaje;

    @Column(name = "FECHA_HORA_ENVIO", nullable = false)
    private String fechaHoraEnvio;

    @Column(name = "NRO_TELEFONO", nullable = false)
    private String nroTelefono;
}