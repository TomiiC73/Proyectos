package com.example.entidades;

import com.example.patron.IAgregado;
import com.example.patron.IIterador;
import com.example.patron.IteradorReseñas;
import com.example.patron.IteradorVinos;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.cglib.core.Local;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "Vinos")
@Data
@AllArgsConstructor
@NoArgsConstructor

public class Vino implements IAgregado {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "añada", nullable = false)
    private String añada;

    @Column(name = "nombre", nullable = false)
    private String nombre;

    @Column(name = "precio", nullable = false)
    private Double precio;

    @ManyToOne
    @JoinColumn(name = "bodega_id", nullable = false)
    private Bodega bodega;

    @ManyToOne
    @JoinColumn(name = "varietal_id", nullable = false)
    private Varietal varietal;

    @OneToMany(mappedBy = "vino")
    private List<Reseña> reseñas;

    public boolean tenesReseñasEnPeriodo(LocalDate[] fechas) {

        Reseña[] reseñasLista = reseñas.toArray(new Reseña[0]);

        boolean estado = false;
        LocalDate fechaDesde = fechas[0];
        LocalDate fechaHasta = fechas[1];

        // Creamos el iterador para las reseñas
        IIterador iteradorReseñas = this.crearIterador(reseñasLista, fechas);
        iteradorReseñas.primero();

        while (!iteradorReseñas.haTerminado()) {
            Reseña reseña = (Reseña) iteradorReseñas.actual();

            if (iteradorReseñas.cumpleFiltro(reseña, new LocalDate[]{fechaDesde, fechaHasta})) {
                estado =  true;
            } else {
                estado = false;
            }
            iteradorReseñas.siguiente();
        }
        return estado;
    }

    public Double calcularPorcentajeDeSomelierEnPeriodo(LocalDate fechaDesde, LocalDate fechaHasta) {
        Integer contador = 0;
        Double acumulador = 0.0;
        Double promedio;

        for (Reseña reseña : this.reseñas) {
            if (reseña.sosDeSomelier() && reseña.sosDePeriodo(fechaDesde, fechaHasta)) {
                acumulador += reseña.getCalificacion();
                contador += 1;
            }
        }

        if (contador > 0) {
            promedio = acumulador / contador;
            promedio = Math.round(promedio * 100.0) / 100.0;
            return promedio;

        } else {
            return 0.0;
        }
    }

    @Override
    public IIterador crearIterador(Object[] elementos, LocalDate[] fechas) {
        Reseña[] reseñasLista = reseñas.toArray(new Reseña[0]);

        IIterador iterador = new IteradorReseñas(reseñasLista, new LocalDate[]{fechas[0], fechas[1]});
        return iterador;
    }
}