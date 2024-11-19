import React, { useState } from "react";
import axios from "axios";

function ReporteForm() {
    // Estado para manejar los datos del formulario
    const [inputDTO, setInputDTO] = useState({
        fechaDesde: "",
        fechaHasta: "",
        tipoReseña: "",
        tipoVisualizacion: "",
    });

    // Estado para controlar si el formulario se muestra o no
    const [mostrarFormulario, setMostrarFormulario] = useState(false); // El formulario inicialmente está oculto

    // Estado para mostrar el modal de confirmación
    const [mostrarModalConfirmacion, setMostrarModalConfirmacion] = useState(false);

    // Estado para mostrar el mensaje de éxito
    const [mensajeExito, setMensajeExito] = useState(false);

    // Función para mostrar el formulario cuando se hace clic en "Generar ranking vinos"
    const mostrarFormularioHandler = () => {
        setMostrarFormulario(true);
    };

    // Función para manejar los cambios en los campos del formulario
    const handleChange = (event) => {
        const { name, value } = event.target;
        setInputDTO({ ...inputDTO, [name]: value });
    };

    // Función para manejar el envío del formulario
    const handleSubmit = async (event) => {
        event.preventDefault();

        // Mostrar el modal de confirmación cuando el usuario haga clic en "Generar reporte"
        setMostrarModalConfirmacion(true);
    };

    // Función para confirmar la generación del reporte
    const confirmarReporte = async () => {
        try {
            const response = await axios.post("http://localhost:8084/vinos/reporte-ranking-vinos", inputDTO);
            console.log(response);

            // Mostrar mensaje de éxito después de que el reporte haya sido generado
            setMensajeExito(true);

            // Cerrar el modal después de la confirmación
            setMostrarModalConfirmacion(false);
            setMostrarFormulario(false); // Opcional: Ocultar el formulario

            // Ocultar el mensaje de éxito después de 3 segundos
            setTimeout(() => setMensajeExito(false), 3000);

        } catch (error) {
            console.error("Error al generar el reporte:", error);
        }
    };

    // Función para cancelar la generación y cerrar el modal
    const cancelarConfirmacion = () => {
        setMostrarModalConfirmacion(false);
    };

    return (
        <div>
            {/* Título de la aplicación */}
            <h1 style={{ textAlign: "center", fontSize: "36px", color: "#890303", marginBottom: "20px" }}>
                BONVINO - Encuentra el vino correcto
            </h1>

            {/* Mostrar el botón para mostrar el formulario */}
            {!mostrarFormulario && (
                <button
                    id="generar-ranking"
                    onClick={mostrarFormularioHandler}
                >
                    Opción generar ranking vinos
                </button>
            )}

            {/* Mostrar el formulario solo cuando el estado mostrarFormulario es true */}
            {mostrarFormulario && (
                <form onSubmit={handleSubmit}>
                    <label>
                        Fecha desde
                        <input
                            type="date"
                            name="fechaDesde"
                            value={inputDTO.fechaDesde}
                            onChange={handleChange}
                        />
                    </label>
                    <br />

                    <label>
                        Fecha hasta
                        <input
                            type="date"
                            name="fechaHasta"
                            value={inputDTO.fechaHasta}
                            onChange={handleChange}
                        />
                    </label>
                    <br />

                    <label>
                        Tipo de reseña
                        <select
                            name="tipoReseña"
                            value={inputDTO.tipoReseña}
                            onChange={handleChange}
                        >
                            <option value="">Seleccionar</option>
                            <option value="premium">Premium</option>
                            <option value="normal">Normal</option>
                            <option value="amigos">Amigos</option>
                        </select>
                    </label>
                    <br />

                    <label>
                        Tipo de visualización
                        <select
                            name="tipoVisualizacion"
                            value={inputDTO.tipoVisualizacion}
                            onChange={handleChange}
                        >
                            <option value="">Seleccionar</option>
                            <option value="excel">Excel</option>
                            <option value="pdf">PDF</option>
                            <option value="pantalla">Pantalla</option>
                        </select>
                    </label>
                    <br />

                    {/* Botón para enviar el formulario */}
                    <button id="generar-reporte" type="submit">
                        Generar reporte
                    </button>
                </form>
            )}

            {/* Modal de confirmación */}
            {mostrarModalConfirmacion && (
                <div className="modal">
                    <h3>¿Está seguro que desea generar el reporte?</h3>
                    <button
                        id="confirmar-reporte"
                        onClick={confirmarReporte}
                    >
                        Sí, generar
                    </button>
                    <button
                        id="cancelar-reporte"
                        onClick={cancelarConfirmacion}
                    >
                        No, cancelar
                    </button>
                </div>
            )}

            {/* Fondo oscuro cuando el modal está visible */}
            {mostrarModalConfirmacion && (
                <div
                    className="modal-overlay"
                    onClick={cancelarConfirmacion}  // Si el usuario hace clic fuera del modal, también lo cierra
                />
            )}

            {/* Mostrar el mensaje de éxito cuando el reporte se haya generado correctamente */}
            {mensajeExito && (
                <div style={{
                    textAlign: "center",
                    marginTop: "20px",
                    fontSize: "18px",
                    color: "#4CAF50", // Verde para indicar éxito
                    backgroundColor: "#DFF2BF", // Fondo suave verde
                    padding: "10px",
                    borderRadius: "5px",
                }}>
                    ¡Reporte generado exitosamente!
                </div>
            )}
        </div>
    );
}

export default ReporteForm;
