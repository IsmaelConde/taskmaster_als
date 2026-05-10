from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import sirope
# IMPORTANTE: Aquí añadimos Category a la lista de importación
from model import User, Project, Task, Category

app = Flask(__name__)
app.secret_key = "clave_secreta_definitiva_als"
s_instance = sirope.Sirope()
login_manager = LoginManager(app)
login_manager.login_view = "login"

# -----------------------------------------------------------------------------
# USUARIOS
# -----------------------------------------------------------------------------

@login_manager.user_loader
def load_user(username):
    usuarios = s_instance.load_all(User)
    for u in usuarios:
        if u.username == username:
            return u
    return None

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form.get("user")
        p = request.form.get("pass")
        usuarios = s_instance.load_all(User)
        user_obj = next((user for user in usuarios if user.username == u), None)
        if user_obj and user_obj.check_password(p):
            login_user(user_obj)
            return redirect(url_for("index"))
        flash("Usuario o contraseña incorrectos")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        u = request.form.get("user")
        p = request.form.get("pass")
        s_instance.save(User(u, p))
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

# -----------------------------------------------------------------------------
# CATEGORÍAS (ENTIDAD 3)
# -----------------------------------------------------------------------------

@app.route("/categories")
@login_required
def list_categories():
    mis_categorias = []
    for oid in s_instance.load_all_keys(Category):
        cat = s_instance.load(oid)
        if cat.user_name == current_user.username:
            mis_categorias.append((s_instance.safe_from_oid(oid), cat))
    return render_template("categories.html", categorias=mis_categorias)

@app.route("/category/add", methods=["POST"])
@login_required
def add_category():
    name = request.form.get("name")
    if name:
        s_instance.save(Category(name, current_user.username))
    return redirect(url_for("list_categories"))

@app.route("/category/delete/<oid>")
@login_required
def delete_category(oid):
    oid_obj = s_instance.oid_from_safe(oid)
    # Si borramos una categoría, los proyectos asociados pasan a "Sin categoría"
    for p_oid in s_instance.load_all_keys(Project):
        p = s_instance.load(p_oid)
        if getattr(p, 'category_oid', None) == oid:
            p.category_oid = None
            s_instance.save(p)
    s_instance.delete(oid_obj)
    return redirect(url_for("list_categories"))

# -----------------------------------------------------------------------------
# PROYECTOS
# -----------------------------------------------------------------------------

@app.route("/")
@login_required
def index():
    proyectos_usuario = []
    oids_reales = s_instance.load_all_keys(Project)
    
    for oid_obj in oids_reales:
        p_obj = s_instance.load(oid_obj)
        if p_obj.user_name == current_user.username:
            oid_texto = s_instance.safe_from_oid(oid_obj)
            
            # Protección para proyectos antiguos
            cat_oid = getattr(p_obj, 'category_oid', None)
            cat_name = "Sin categoría"
            
            if cat_oid:
                try:
                    cat_obj = s_instance.load(s_instance.oid_from_safe(cat_oid))
                    cat_name = cat_obj.name
                except:
                    p_obj.category_oid = None
                    s_instance.save(p_obj)
            
            proyectos_usuario.append((oid_texto, p_obj, cat_name))
            
    # Listar categorías para el desplegable del formulario
    categorias_form = []
    for c_oid in s_instance.load_all_keys(Category):
        c = s_instance.load(c_oid)
        if c.user_name == current_user.username:
            categorias_form.append((s_instance.safe_from_oid(c_oid), c))

    return render_template("index.html", proyectos=proyectos_usuario, categorias=categorias_form)

@app.route("/project/add", methods=["POST"])
@login_required
def add_project():
    name = request.form.get("name")
    desc = request.form.get("desc")
    cat_oid = request.form.get("category_oid")
    nuevo_p = Project(name, desc, current_user.username, cat_oid)
    s_instance.save(nuevo_p)
    return redirect(url_for("index"))

@app.route("/project/<oid>")
@login_required
def view_project(oid):
    oid_objeto = s_instance.oid_from_safe(oid)
    project = s_instance.load(oid_objeto)
    
    # Parches de seguridad para objetos viejos
    if not hasattr(project, 'completed'): project.completed = False
    if not hasattr(project, 'category_oid'): project.category_oid = None

    tareas_proyecto = []
    for t_oid_obj in s_instance.load_all_keys(Task):
        t_obj = s_instance.load(t_oid_obj)
        if t_obj.project_oid == oid:
            t_safe = s_instance.safe_from_oid(t_oid_obj)
            tareas_proyecto.append((t_safe, t_obj))
            
    return render_template("project.html", p=project, tareas=tareas_proyecto, p_oid=oid)

@app.route("/project/toggle/<p_oid>")
@login_required
def toggle_project(p_oid):
    oid_obj = s_instance.oid_from_safe(p_oid)
    project = s_instance.load(oid_obj)
    project.completed = not getattr(project, 'completed', False)
    s_instance.save(project)
    return redirect(url_for("index"))

@app.route("/project/edit/<p_oid>", methods=["GET", "POST"])
@login_required
def edit_project(p_oid):
    oid_obj = s_instance.oid_from_safe(p_oid)
    project = s_instance.load(oid_obj)
    if request.method == "POST":
        project.name = request.form.get("name")
        project.description = request.form.get("desc")
        s_instance.save(project)
        return redirect(url_for("index"))
    return render_template("edit_project.html", p=project, p_oid=p_oid)

@app.route("/project/delete/<p_oid>")
@login_required
def delete_project(p_oid):
    for t_oid_obj in s_instance.load_all_keys(Task):
        t_obj = s_instance.load(t_oid_obj)
        if t_obj.project_oid == p_oid:
            s_instance.delete(t_oid_obj)
    oid_obj = s_instance.oid_from_safe(p_oid)
    s_instance.delete(oid_obj)
    return redirect(url_for("index"))

# -----------------------------------------------------------------------------
# TAREAS
# -----------------------------------------------------------------------------

@app.route("/task/add/<p_oid>", methods=["POST"])
@login_required
def add_task(p_oid):
    content = request.form.get("content")
    s_instance.save(Task(content, p_oid))
    return redirect(url_for("view_project", oid=p_oid))

@app.route("/task/toggle/<t_oid>/<p_oid>")
@login_required
def toggle_task(t_oid, p_oid):
    oid_obj = s_instance.oid_from_safe(t_oid)
    task = s_instance.load(oid_obj)
    task.completed = not getattr(task, 'completed', False)
    s_instance.save(task)
    return redirect(url_for("view_project", oid=p_oid))

@app.route("/task/edit/<t_oid>/<p_oid>", methods=["POST"])
@login_required
def edit_task(t_oid, p_oid):
    oid_obj = s_instance.oid_from_safe(t_oid)
    task = s_instance.load(oid_obj)
    task.content = request.form.get("content")
    s_instance.save(task)
    return redirect(url_for("view_project", oid=p_oid))

@app.route("/task/delete/<t_oid>/<p_oid>")
@login_required
def delete_task(t_oid, p_oid):
    oid_obj = s_instance.oid_from_safe(t_oid)
    s_instance.delete(oid_obj)
    return redirect(url_for("view_project", oid=p_oid))

if __name__ == "__main__":
    app.run(debug=True)