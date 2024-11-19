package com.example.entidades;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Entity
@Table(name = "Reseñas")
@Data
@NoArgsConstructor
@AllArgsConstructor

public class Reseña {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "fecha_reseña", nullable = false)
    private String fechaReseña; // Almacena como String en formato YYYY-MM-DD

    @Column(name = "tipo_reseña", nullable = false)
    private String tipoReseña;

    @Column(name = "calificacion", nullable = false)
    private Long calificacion;

    @ManyToOne
    @JoinColumn(name = "vino_id")
    private Vino vino;

    public LocalDate getFechaReseñaAsLocalDate() {
        return LocalDate.parse(fechaReseña); // Convierte de String a LocalDate
    }

    public boolean sosDePeriodo(LocalDate fechaDesde, LocalDate fechaHasta) {
        LocalDate fecha = getFechaReseñaAsLocalDate();
        return (fechaDesde.isBefore(fecha) || fechaDesde.isEqual(fecha)) &&
                (fechaHasta.isAfter(fecha) || fechaHasta.isEqual(fecha));
    }

    public boolean sosDeSomelier() {
        return "premium".equals(this.tipoReseña);
    }
}