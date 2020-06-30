from flask import Flask, render_template, request, redirect, url_for, session 
import requests as req

# creamos una instancia de la clase Flask que obtiene como valor la cadena "__main__"
app = Flask(__name__)

#creamos una clave secreta para utilizar las coquies 
app.secret_key = 'key-secret'


# MODULO INVITADO

# definimos una funcion que renderiza nuestro index.html - landingpage
# y esta función esta asignada a la URL '/' de inicio
@app.route('/')
def index():
    if 'token' in session:
        key = session['token']
    else:
        key = ''
    return render_template('index.html', token= key)

# definimos una funcion que renderiza   nuestro portafolio.html 
# y esta función esta asignada a la URL '/portafolio' 
# hacemos la consulta para traer todos las propiedas
# y tambien hacemos una condición del token para unas validaciones en nuestro html
@app.route('/portafolio')
def portafolio():    
    response = req.get('http://localhost:3001/properties')
    if response.status_code == 200:
        result = response.json()                
        if 'token' in session:
            key = session['token']
        else:
            key = ''
    else:
        print('mal')
    return render_template('portfolio.html', properties =  result['data'], token = key )

# definimos una funcion que renderiza   nuestro propertydetails.html 
# y esta función esta asignada a la URL '/propertydetails' 
# hacemos una condicion - si esque existe el token para las validaciones de rutas en nuestro html
# hacemos la consulta para traer una propiedad por su id
@app.route('/property-detail')
def propertyDetail():
    id = request.args.get('id')
    if 'token' in session:
        response = req.get(f'http://localhost:3001/property/{id}')
        if response.status_code == 200:
            result = response.json()               
            return render_template('propertydetails.html', property=result['data'], token= session['token'] )
        else:
            print('mall')
    else:
        return redirect(url_for('portafolio'))

# definimos la function filterpriceadmin y le asignamos la ruta de /filterpriceadmin   
# preguntamos si existe el token del usuario para manejarlo en nuestra consulta
# hacemos consulta enviandole el token en los headers
# si todo esta bien renderizamos properties.html donde le enviamos la data nueva filtrada
@app.route('/filterprice')
def filterprice():
        response = req.get('http://localhost:3001/properties/price')
        if response.status_code == 200:
            result = response.json()
            if 'token' in session:
                key = session['token']
            else:
                key = ''
            return render_template('portfolio.html', properties =  result['data'], token = key )
        else:
            print('null')


# definimos una funcion que renderiza   nuestro reguistro.html 
# y esta función esta asignada a la URL '/registro' 
# hacemos una condicion - si esque existe el token para las validaciones de rutas en nuestro html
@app.route('/registro')
def registro():
    if 'token' in session:        
        return redirect(url_for('portafolio'))
    else:
        return render_template('reguistro.html')

# definimos una funcion que cumple una acción de nuestro formulario de registro
# y esta función esta asignada a la URL '/register
# le decimos que acepte solo metodo POST  'methods=['POST']' 
# request.form = obtenemos valores de nuestros inputs deacuerdo a su atributo name 
# le enviamos el diccionario a la consulta 
# y nos redireccionamos al login para que el usuario pueda logearse
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    lastname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']
    addRegister = {"name": name, "lastname": lastname, "email": email, "password":password}
    response = req.post('http://localhost:3001/user', json= addRegister )
    result = response.json()
    return redirect(url_for('login'))

# definimos una funcion que renderiza   nuestro login.html 
# y esta función esta asignada a la URL '/login' 
# hacemos una condicion - si esque existe el token para las validaciones de rutas en nuestro html
@app.route('/login')
def login():
    if 'token' in session:
        return redirect(url_for('portafolio'))
    else:
        return render_template('login.html')

# definimos una funcion que cumple una acción de nuestro formulario de login
# y esta función esta asignada a la URL '/logeo
# le decimos que acepte solo metodo POST  'methods=['POST']' 
# request.form = obtenemos valores de nuestros inputs deacuerdo a su atributo name 
# le enviamos el diccionario a la consulta 
# creamos una coquie llamada 'token' y le asignamos el valor del token
# y nos redireccionamos al portafolio para que el usuario pueda ver los detalles de los inmuebles
# status_code = 200 |  OK
@app.route('/logeo', methods=['POST'])
def logeo():
    email = request.form['email']    
    password = request.form['password']
    addLogged = {"email": email, "password": password}
    response = req.post('http://localhost:3001/login', json= addLogged)
    if response.status_code == 200:
        result = response.json()
        session['token'] = result['token']
        return redirect(url_for('portafolio'))
    else: 
        return render_template('erroruser.html')

# definimos una funcion que cumple una acción de nuestro button - cerrar sesión
# y esta función esta asignada a la URL '/logout
# verificamos si existe le token del usuario
# eliminamos el token
# y nos redireccionamos al index - landinpage
@app.route('/logout')
def logout():
    if 'token' in session:
        session.pop('token', None)
        return redirect(url_for('index'))

# MODULO ADMINISTRADOR

# definimos una funcion que renderiza   nuestro registeradmin.html 
# y esta función esta asignada a la URL '/registeradmin' 
# hacemos una condicion - si esque existe el token 'superuser' para las validaciones de rutas en nuestro html
@app.route('/registeradmin')
def registeradmin():
    if 'superuser' in session:
        return redirect(url_for('admin'))
    else:
        return render_template('registeradmin.html')

# definimos una funcion que cumple una acción de nuestro formulario de registeradminform
# y esta función esta asignada a la URL '/registeradminform
# le decimos que acepte solo metodo POST  'methods=['POST']' 
# request.form = obtenemos valores de nuestros inputs deacuerdo a su atributo name 
# le enviamos el diccionario a la consulta 
# y nos redireccionamos al login - loginadmin.html para que el usuario pueda logearse
# status_code = 200 |  OK
@app.route('/registeradminform', methods=['POST'])
def registeradminform():
    name = request.form['name']
    lastname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']
    addRegister = {"name": name, "lastname": lastname, "email": email, "password":password, "role": "ADMIN_ROLE"}
    response = req.post('http://localhost:3001/user', json= addRegister )
    if response.status_code == 200:
        result = response.json()
        return redirect(url_for('loginadmin'))

# definimos una funcion que renderiza   nuestro loginadmin.html 
# y esta función esta asignada a la URL '/loginadmin' 
# hacemos una condicion - si esque existe el token 'superuser' para las validaciones de rutas en nuestro html
@app.route('/loginadmin')
def loginadmin():
    if 'superuser' in session:
        return redirect(url_for('admin'))
    else:
        return render_template('loginadmin.html')

# definimos una funcion que cumple una acción de nuestro formulario de loginadminuser
# y esta función esta asignada a la URL '/loginadminuser
# le decimos que acepte solo metodo POST  'methods=['POST']' 
# request.form = obtenemos valores de nuestros inputs deacuerdo a su atributo name 
# le enviamos el diccionario a la consulta 
# creamos una coquie llamada 'superuser' y le asignamos el valor del token
# y nos redireccionamos al admin - propierties.html para que el usuario pueda ver sus inmuebles que tiene
# status_code = 200 |  OK
@app.route('/loginadminuser', methods=['POST'])
def loginadminuser():
    email = request.form['email']    
    password = request.form['password']
    addLogged = {"email": email, "password": password}
    response = req.post('http://localhost:3001/login', json= addLogged)
    if response.status_code == 200:
        result = response.json()
        session['superuser'] = result['token']
        return redirect(url_for('admin'))
    else:
        return render_template('erroradmin.html')

# definimos una funcion que renderiza   nuestro properties.html si se cumple todas las condiciones
# y esta función esta asignada a la URL '/admin' 
# hacemos una condicion - si esque existe el token 'superuser' para las validaciones de rutas en nuestro html
@app.route('/admin')
def admin():
    if 'superuser' in session :
        token = session['superuser']
        headers = {"token": token }
        response = req.get('http://localhost:3001/propertiesadmin', headers= headers)
        if response.status_code == 200:
            result = response.json()
            return render_template('properties.html', properties =  result['data'])
        else:
            session.pop('superuser',None)
            return render_template('erroradmin.html')
    else :
        return redirect(url_for('loginadmin'))

# definimos la function filterpriceadmin y le asignamos la ruta de /filterpriceadmin   
# preguntamos si existe el token del usuario para manejarlo en nuestra consulta
# hacemos consulta enviandole el token en los headers
# si todo esta bien renderizamos properties.html donde le enviamos la data nueva filtrada
@app.route('/filterpriceadmin')
def filterpriceadmin():
    if 'superuser' in session:
        token = session['superuser']
        headers = {"token": token }
        response = req.get('http://localhost:3001/properties/priceadmin', headers= headers)
        if response.status_code == 200:
            result = response.json()
            return render_template('properties.html', properties =  result['data'])
        else:
            print('null')
    else:
        return redirect(url_for('loginadmin'))


# definimos una funcion que renderiza   nuestro editproperty.html si se cumplen todas las condiciones
# y esta función esta asignada a la URL '/edit' 
# hacemos una condicion - si esque existe el token 'superuser' para utilizar dicho token en nuestra consulta
# hacemos la peticion get para traer dicho inmueble por su id, y en sus headers le mandamos el token
@app.route('/edit')
def edit():
    id = request.args.get('id')
    if 'superuser' in session:
        token = session['superuser']
        headers = {"token": token}
        response = req.get(f'http://localhost:3001/property/{id}', headers = headers)
        if response.status_code == 200 :
            result = response.json()
            return render_template('editproperty.html', property = result['data'])
        else:
            print('mallll') 
    else:
        return render_template('loginadmin')

# definimos una funcion que renderiza   nuestro propierties.html si se cumplen todas las condiciones
# y esta función esta asignada a la URL '/editproperty' 
# hacemos una condicion - si esque existe el token 'superuser' para utilizar dicho token en nuestra consulta
# obtenemos el valor del token y lo guardamos en nuestros headers
# obtenemos el valor de los inputs del formulario
# hacemos la consulta put enviando los headers y el diccionario creado
@app.route('/editproperty', methods=['POST'])
def editproperty():
    id = request.args.get('id')
    if 'superuser' in session:
        token = session['superuser']
        headers = {"token": token}
        title = request.form['title']    
        tipo = request.form['type']
        address = request.form['address']
        rooms = request.form['rooms']
        price = request.form['price']
        area = request.form['area']
        updateProperty = {"title": title, "type": tipo, "address": address, "rooms":rooms, "price": price, "area":area}
        response = req.put(f'http://localhost:3001/property/{id}', headers= headers, json=updateProperty)
        if response.status_code == 200 :
            return redirect(url_for('admin'))
        else:
            print('mallll')            
    else :
        return redirect(url_for('loginadmin'))

# definimos una funcion que renderiza   nuestro addproperty.html si se cumplen todas las condiciones
# y esta función esta asignada a la URL '/add' 
# hacemos una condicion - si esque existe el token 'superuser' para las validaciones de rutas en nuestro html@app.route('/add')
@app.route('/add')
def add():
    if 'superuser' in session:
        return render_template('addproperty.html')
    else:
        return redirect(url_for('loginadmin'))

# definimos una funcion que renderiza   nuestro addproperty.html si se cumplen todas las condiciones
# y esta función esta asignada a la URL '/addproperty' 
# hacemos una condicion - si esque existe el token 'superuser' para utilizar dicho token en nuestra consulta
# obtenemos el valor del token y lo guardamos en nuestros headers
# obtenemos el valor de los inputs del formulario
# hacemos la consulta post enviando los headers y el diccionario creado
@app.route('/addproperty', methods=['POST'] )
def addproperty():
    if 'superuser' in session:
        token = session['superuser']
        headers = {"token": token}
        title = request.form['title']    
        tipo = request.form['type']
        address = request.form['address']
        rooms = request.form['rooms']
        price = request.form['price']
        area = request.form['area']
        addProperty = {"title": title, "type": tipo, "address": address, "rooms":rooms, "price": price, "area":area}
        response = req.post('http://localhost:3001/property/', headers= headers, json=addProperty)
        if response.status_code == 201:
            return redirect(url_for('admin'))
        else:
            print('mall')
    else:
        return redirect(url_for('loginadmin'))

 
# definimos una funcion que cumple una acción de nuestro button - eliminar propiedad
# y esta función esta asignada a la URL '/delete
# verificamos si existe le token del usuario 'superuser'
# hacemos la consulta donde enviamos el id que recibimos de los parametros y tbm le enviamos los headers
# si todo esta bien nos redireccionamos a nuestro propierties.html funcion - admin
@app.route('/delete')
def delete():
    id = request.args.get('id')
    if 'superuser' in session:
        token = session['superuser']
        headers = {"token": token}
        response = req.delete(f'http://localhost:3001/property/{id}', headers=headers)
        if response.status_code == 200:
            return redirect(url_for('admin'))
        else :
            print('malll')
    else:
        return redirect(url_for('loginadmin'))

# definimos una funcion que cumple una acción de nuestro button - cerrar sesión
# y esta función esta asignada a la URL '/signoff
# verificamos si existe le token del usuario 'superuser'
# eliminamos el token 'superuser'
# y nos redireccionamos al loginadmin
@app.route('/signoff')
def signoff():
    if 'superuser' in session:
        session.pop('superuser', None)
        return redirect(url_for('loginadmin'))

# si la condicion es correcta corremos nuestro aplicacion
# el debug = true, nos facilita poder rastrear los errores.
if __name__ == "__main__":
    app.run(debug=True)