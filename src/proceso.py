class Proceso:
    # Conjunto estático para almacenar los PIDs utilizados
    _pids_usados = set()

    def __init__(self, pid: str, duracion: int, prioridad: int):
        """
        Inicializa un nuevo proceso con los atributos especificados.
        
        Args:
            pid (str): Identificador único del proceso.
            duracion (int): Tiempo total de CPU requerido.
            prioridad (int): Valor de prioridad (menor valor = mayor prioridad).
        
        Raises:
            ValueError: Si los argumentos son inválidos o el PID está duplicado.
        """
        # Validaciones
        if not isinstance(pid, str) or not pid.strip():
            raise ValueError("El PID debe ser una cadena no vacía")
        if pid in Proceso._pids_usados:
            raise ValueError(f"El PID '{pid}' ya está en uso")
        if not isinstance(duracion, int) or duracion <= 0:
            raise ValueError("La duración debe ser un entero positivo")
        if not isinstance(prioridad, int) or prioridad < 0:
            raise ValueError("La prioridad debe ser un entero no negativo")

        # Registrar el PID
        Proceso._pids_usados.add(pid)

        # Atributos básicos
        self._pid = pid
        self._duracion = duracion
        self._prioridad = prioridad

        # Atributos adicionales
        self._tiempo_restante = duracion  # Tiempo de CPU restante
        self._tiempo_llegada = 0  # Asumido como 0 para simplificación
        self._tiempo_inicio = None  # Se establecerá cuando el proceso comience
        self._tiempo_fin = None  # Se establecerá cuando el proceso termine

    def __del__(self):
        """
        Libera el PID cuando el objeto es destruido.
        """
        if self._pid in Proceso._pids_usados:
            Proceso._pids_usados.remove(self._pid)

    # Propiedades para acceder a los atributos
    @property
    def pid(self) -> str:
        return self._pid

    @property
    def duracion(self) -> int:
        return self._duracion

    @property
    def prioridad(self) -> int:
        return self._prioridad

    @property
    def tiempo_restante(self) -> int:
        return self._tiempo_restante

    @property
    def tiempo_llegada(self) -> int:
        return self._tiempo_llegada

    @property
    def tiempo_inicio(self) -> int:
        return self._tiempo_inicio

    @property
    def tiempo_fin(self) -> int:
        return self._tiempo_fin

    # Métodos para modificar atributos controladamente
    def reducir_tiempo_restante(self, tiempo: int) -> None:
        """
        Reduce el tiempo restante del proceso.
        
        Args:
            tiempo (int): Cantidad de tiempo a reducir.
        
        Raises:
            ValueError: Si el tiempo es inválido o excede el tiempo restante.
        """
        if not isinstance(tiempo, int) or tiempo <= 0:
            raise ValueError("El tiempo a reducir debe ser un entero positivo")
        if tiempo > self._tiempo_restante:
            raise ValueError("El tiempo a reducir excede el tiempo restante")
        self._tiempo_restante -= tiempo

    def establecer_tiempo_inicio(self, tiempo: int) -> None:
        """
        Establece el tiempo de inicio del proceso.
        
        Args:
            tiempo (int): Tiempo de inicio.
        
        Raises:
            ValueError: Si el tiempo es inválido o ya está establecido.
        """
        if not isinstance(tiempo, int) or tiempo < 0:
            raise ValueError("El tiempo de inicio debe ser un entero no negativo")
        if self._tiempo_inicio is not None:
            raise ValueError("El tiempo de inicio ya está establecido")
        self._tiempo_inicio = tiempo

    def establecer_tiempo_fin(self, tiempo: int) -> None:
        """
        Establece el tiempo de finalización del proceso.
        
        Args:
            tiempo (int): Tiempo de finalización.
        
        Raises:
            ValueError: Si el tiempo es inválido o ya está establecido.
        """
        if not isinstance(tiempo, int) or tiempo < 0:
            raise ValueError("El tiempo de finalización debe ser un entero no negativo")
        if self._tiempo_fin is not None:
            raise ValueError("El tiempo de finalización ya está establecido")
        self._tiempo_fin = tiempo

    def __str__(self) -> str:
        """
        Representación en cadena del proceso.
        """
        return (f"Proceso(pid={self._pid}, duracion={self._duracion}, "
                f"prioridad={self._prioridad}, tiempo_restante={self._tiempo_restante})")