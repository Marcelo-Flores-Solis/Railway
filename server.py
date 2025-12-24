import http.server
import socketserver
import os
import mimetypes
from urllib.parse import parse_qs

# IMPORTAMOS NUESTRO NUEVO ARCHIVO
import database.db_manager as db_manager 

PORT = int(os.environ.get("PORT", 8000))
TEMPLATE_DIR = 'templates'
ASSET_DIR = 'assets'

class MiSitioHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        path = self.path.rstrip('/')
        if path == '':
            path = '/'

        rutas = {
            '/': 'index.html',
            '/contacto': 'contacto.html',
            '/login': 'login.html',
            '/ajedrez': 'aprendeAlgo/ajedrez.html',
            '/piano': 'aprendeAlgo/piano.html',
            '/juegos': 'diviertete/juegos.html',
            '/musica': 'diviertete/musica.html',
            '/series': 'diviertete/series.html'
        }

        try:
            if self.path.startswith('/assets/'):
                self.servir_statico()
                return

            # CASO ESPECIAL: ADMIN
            if path == '/admin':
                archivo_path = os.path.join(TEMPLATE_DIR, 'admin.html')
                with open(archivo_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # USAMOS DB_MANAGER PARA LEER LOS DATOS
                filas = db_manager.obtener_mensajes()
                
                content = content.replace('{FILAS_TABLA}', filas)
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
                return

            if path in rutas:
                archivo_path = os.path.join(TEMPLATE_DIR, rutas[path])
                self.servir_html(archivo_path)
            else:
                self.send_error(404, "Pagina no encontrada")

        except Exception as e:
            print(f"Error: {e}")
            self.send_error(500, f"Error interno: {e}")

    def do_POST(self):
        if self.path == '/enviar-contacto':
            self.manejar_contacto()
        elif self.path == '/login': 
            self.manejar_login() 
        else:
            self.send_error(404, "Ruta POST no valida")

    def servir_html(self, path_archivo):
        try:
            with open(path_archivo, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, "HTML no encontrado")

    def servir_statico(self):
        path_archivo = self.path[1:] 
        try:
            with open(path_archivo, 'rb') as f:
                content = f.read()
            mime_type, _ = mimetypes.guess_type(path_archivo)
            self.send_response(200)
            if mime_type:
                self.send_header('Content-type', mime_type)
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, "Archivo no encontrado")

    def manejar_contacto(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        datos = parse_qs(post_data)
        
        nombre = datos.get('nombre', [''])[0]
        email = datos.get('email', [''])[0]
        mensaje = datos.get('mensaje', [''])[0]
        
        print(f"Recibido: {nombre}")

        # USAMOS DB_MANAGER PARA GUARDAR
        db_manager.guardar_mensaje(nombre, email, mensaje)

        self.send_response(303) 
        self.send_header('Location', '/')
        self.end_headers()

    def manejar_login(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        datos = parse_qs(post_data)

        username = datos.get('username', [''])[0]
        password = datos.get('password', [''])[0]

        if username == "admin" and password == "123":
            self.send_response(303)
            self.send_header('Location', '/admin')
            self.end_headers()
        else:
            self.send_response(303)
            self.send_header('Location', '/login')
            self.end_headers()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with socketserver.TCPServer(("", PORT), MiSitioHandler) as httpd:
        print(f"Servidor corriendo en http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()