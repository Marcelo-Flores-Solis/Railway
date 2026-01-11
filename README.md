# Pagina Personal

### Enlaces del Proyecto
* **Sitio Web en Vivo (Railway):** https://web-production-4c97e.up.railway.app/
* **Repositorio:** https://github.com/Marcelo-Flores-Solis/Railway

---

### Descripción
Aplicación web **Full Stack** desarrollada como proyecto final para el curso de Introducción al Desarrollo Web (UNSA).

El proyecto destaca por implementar una arquitectura **cliente-servidor desde cero**. En lugar de utilizar frameworks de alto nivel (como Flask o Django), el backend ha sido construido utilizando librerías nativas de Python (`http.server`) para gestionar el enrutamiento y las peticiones HTTP manualmente. El sistema cuenta con persistencia de datos en la nube mediante **MySQL**, un panel de administración seguro con estadísticas en tiempo real y módulos interactivos en el frontend.

### Características Principales
* **Backend Nativo:** Servidor HTTP personalizado escrito en Python puro.
* **Base de Datos Cloud:** Conexión remota a MySQL alojada en Railway.
* **Panel de Administración (Dashboard):**
    * Acceso protegido por Login.
    * Visualización de mensajes de contacto.
    * Métricas en tiempo real (Total de mensajes, Usuarios únicos).
* **Interactividad:** Piano virtual con Web Audio API y formulario de contacto funcional.

---

### Tecnologías Utilizadas

#### Frontend
* **HTML5:** Estructura semántica.
* **CSS3:** Diseño responsivo, Grid/Flexbox y animaciones personalizadas.
* **JavaScript (ES6):** Lógica del cliente, validaciones y sintetizador de audio.

#### Backend
* **Python 3:** Lógica del servidor y manejo de rutas (`http.server`, `socketserver`).
* **MySQL Connector:** Gestión de conexiones y consultas SQL.

#### Infraestructura
* **Railway:** Plataforma de despliegue (PaaS) y alojamiento de Base de Datos.
* **Git & GitHub:** Control de versiones.

---

### Credenciales de Acceso (Demo)
Para probar el panel de administración, puedes acceder a la ruta `/login` 

* **Usuario:** `admin`
* **Contraseña:** `123`
