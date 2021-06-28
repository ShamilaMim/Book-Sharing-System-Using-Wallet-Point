import sqlite3
import os
import os.path
from flask import Flask,render_template,request,redirect,session,url_for,send_from_directory
from flask import Flask
from flask_wtf import file
from werkzeug.utils import secure_filename
import sys
from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
# import sqlite3 as sql
# from sqlalchemy.testing import db

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))+ '/static/profile'
UPLOAD_POST = os.path.dirname(os.path.abspath(__file__))+ '/static/image'
# file.save(os.path.join(/static/profile/, filename))
ALLOWED_EXTENSIONS = {'jpg', 'jpeg','png','JPG','JPEG','PNG'}
app = Flask(__name__) # you also use any object name
app.secret_key = "super secret key"



# DIR_PATH = os.path.dirname(os.path.realpath(__file__))
print(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_POST'] = UPLOAD_POST

# limit upload size upto 8mb
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# application = Flask(__name__)

@app.route("/upload1", methods=['GET', 'POST'])
def upload():
    # file = request.files['file']
    # print(file)
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            path = (os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("path :", path)
            
        print("fname :", filename)
        filename1 = " ".join(filename)

    return render_template('createPost.html')

@app.route("/upload", methods=['GET', 'POST'])
def upl():
    if request.method == 'POST':
        file=request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        path = (os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return render_template('upload.html', f=file.filename)
    return render_template('upload.html')

@app.route('/profileimage/<int:id>', methods=['GET', 'POST'])
def profieimage(id):
    if request.method == 'POST':
        id=session["id"]
        file=request.files['file']
        image=file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        path = (os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        db = sqlite3.connect('project.db')  
        cursor = db.cursor()
        query="UPDATE user SET userimage=? where id=?"
        cursor.execute(query,(image,id,))
        db.commit()
        db.close()
        return redirect(url_for("profile"))
    id=session["id"]
    con = sqlite3.connect('project.db')
    con.row_factory=sqlite3.Row
    c = con.cursor()  # cursor
    # read question : SQLite index startba from 1 (see index.html)
    query = "SELECT * FROM user where id=?"
    c.execute(query,(id,))
    rows = c.fetchall()  # fetch the data from cursor
    con.commit()  # apply changes
    return render_template("profile.html",rows=rows)
    

@app.route("/index")
def index():
    con = sqlite3.connect('project.db')
    con.row_factory=sqlite3.Row
    c = con.cursor()  # cursor
    # read question : SQLite index startba from 1 (see index.html)
    query = "SELECT * FROM category"
    query1 = "SELECT * FROM post"
    c.execute(query)
    rows = c.fetchall()  # fetch the data from cursor
    c.execute(query1)
    rows2=c.fetchall()
    print(rows2)
    rows2.reverse()
    con.commit()  # apply changes
    con.close()
    return render_template("index.html",rows=rows,rows2=rows2)

@app.route("/home")
def home():
    con = sqlite3.connect('project.db')
    con.row_factory=sqlite3.Row
    c = con.cursor()  # cursor
    # read question : SQLite index startba from 1 (see index.html)
    query = "SELECT * FROM category"
    query1 = "SELECT * FROM post"
    c.execute(query)
    rows = c.fetchall()  # fetch the data from cursor
    print(rows)
    c.execute(query1)
    rows2=c.fetchall()
    print(rows2)
    rows2.reverse()
    #notification
    id=session["id"]
    print(id)
    query3 = "SELECT * FROM post INNER JOIN bookrequest ON post.id= bookrequest.postId where post.userId=? or requserId=?"
    c.execute(query3,(id,id,))
    noti = c.fetchall()  # fetch the data from cursor
    print(noti)
    noti.reverse()
    con.commit()  # apply changes
    con.close()
    ID=str(id)
    return render_template("home.html",rows=rows,rows2=rows2,noti=noti,ID=ID)

@app.route("/<int:id>")
def categorybook(id):
    con = sqlite3.connect('project.db')
    con.row_factory=sqlite3.Row
    c = con.cursor()  # cursor
    # read question : SQLite index startba from 1 (see index.html)
    query = "SELECT * FROM category"
    query1 = "SELECT * FROM post where categoryId=?"
    c.execute(query)
    rows = c.fetchall()  # fetch the data from cursor
    c.execute(query1,(id,))
    rows2=c.fetchall()
    print(rows2)
    rows2.reverse()
    con.commit()  # apply changes
    con.close()
    return render_template("index.html",rows=rows,rows2=rows2)


@app.route("/home/<int:id>")
def categoryBook(id):
    con = sqlite3.connect('project.db')
    con.row_factory=sqlite3.Row
    c = con.cursor()  # cursor
    # read question : SQLite index startba from 1 (see index.html)
    query = "SELECT * FROM category"
    query1 = "SELECT * FROM post where categoryId=?"
    c.execute(query)
    rows = c.fetchall()  # fetch the data from cursor
    c.execute(query1,(id,))
    rows2=c.fetchall()
    print(rows2)
    rows2.reverse()
    #notification
    id=session["id"]
    query3 = "SELECT * FROM post INNER JOIN bookrequest ON post.id= bookrequest.postId where post.userId=? or requserId=?"
    c.execute(query3,(id,id,))
    noti = c.fetchall()  # fetch the data from cursor
    print(noti)
    con.commit()  # apply changes
    con.close()
    ID=str(id)
    return render_template("home.html",rows=rows,rows2=rows2,noti=noti,ID=ID)
    


@app.route('/book/<int:id>')
def indexpost(id):
    con = sqlite3.connect('project.db')
    con.row_factory=sqlite3.Row
    c = con.cursor()  # cursor
    query = "SELECT * FROM post WHERE id=?"
    c.execute(query,(id,))
    rows = c.fetchall()  # fetch the data from cursor
    con.commit()  # apply changes
    con.close()
    return render_template("indexpost.html",rows=rows)



@app.route('/post/<int:id>',methods=['GET', 'POST'])
def post(id):
    if request.method=="POST":
        requestName = session["name"]
        requserId=session["id"]
        userId = request.form.get("userid")
        postId = request.form.get("postid")
        status=1
        wallet = request.form.get("wallet")
        process = "pending"
        db = sqlite3.connect('project.db')
        c = db.cursor()
        c.execute("INSERT INTO bookrequest(postId, userId,requserId,bookstatus, requserName,reqWallet,process) VALUES (?,?,?,?,?,?,?)" , (postId,userId,requserId,status,requestName,wallet,process))
        query = "SELECT wallet FROM user WHERE id=?"
        c.execute(query,(requserId,))
        rows = c.fetchall()
        for i in rows:
            value= int(i[0])
            wallet=int(wallet)
            result=value-wallet
            query="UPDATE user SET wallet=? where id=?"
            c.execute(query,(result,requserId,))
        db.commit()
        db.close()
        return redirect("/home")
    con = sqlite3.connect('project.db')
    con.row_factory=sqlite3.Row
    c = con.cursor()  # cursor
    query = "SELECT * FROM post WHERE id=?"
    c.execute(query,(id,))
    rows = c.fetchall()  # fetch the data from cursor
    loginId=session["id"]
    query2 = "SELECT wallet FROM user where id=?"
    c.execute(query2,(loginId,))
    rows3=c.fetchall()
    print(rows3)
    for i in rows3:
        userWallet=i[0]
    con.commit()  # apply changes
    con.close()
    return render_template("post.html",rows=rows,userWallet=userWallet,loginId=loginId)



@app.route("/createpost",methods=['GET', 'POST'])
def createPost():
    if session["login"]:
        con = sqlite3.connect('project.db')
        c = con.cursor() 
        if request.method=="POST":
            name = session["name"]
            userid=session["id"]
            post = request.form.get("post")
            title = request.form.get("title")
            prize=request.form.get("prize")
            wallet=request.form.get("wallet")
            area=request.form.get("location")
            category=request.form.get("category")
            query1="SELECT id FROM category WHERE name=?"
            c.execute(query1,(category,))
            r = c.fetchall()
            for i in r:
                categoryId=i[0]
            status=1
            time=str(datetime.utcnow())
            file=request.files['file']
            image=file.filename
            file.save(os.path.join(app.config['UPLOAD_POST'], file.filename))
            path = (os.path.join(app.config['UPLOAD_POST'], file.filename))
            db = sqlite3.connect('project.db')
            c = db.cursor()
            c.execute("INSERT INTO post(pusername, post, title, orginalprize, wallet, area, time, status, image, category,userId,categoryId) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)" , (name, post,title,prize,wallet,area,time,status,image,category,userid,categoryId))
            db.commit()
            db.close()
            return redirect("/home")
        con.row_factory=sqlite3.Row
        c = con.cursor()  # cursor
        query = "SELECT * FROM category"
        c.execute(query)
        rows = c.fetchall()  # fetch the data from cursor
        con.commit()  # apply changes
        con.close()
        return render_template("createPost.html",rows=rows)
    else:
        return redirect("/home")


@app.route("/notification")
def notification():
    if session["login"]:
        id=session["id"]
        con = sqlite3.connect('project.db')
        con.row_factory=sqlite3.Row
        c = con.cursor()  # cursor
        query = "SELECT * FROM post INNER JOIN bookrequest ON post.id= bookrequest.postId where post.userId=? or requserId=?"
        c.execute(query,(id,id,))
        rows = c.fetchall()  # fetch the data from cursor
        con.commit()  # apply changes
        con.close()
        ID=str(id)
        return render_template("notification.html",rows=rows,ID=ID)


@app.route("/accept/<int:id>")
def accept(id):
    if session["login"]:
        userid=session["id"]
        db = sqlite3.connect('project.db')  
        cursor = db.cursor()
        query1="SELECT reqWallet,postId FROM bookrequest WHERE reqId=?"
        cursor.execute(query1,(id,))
        r = cursor.fetchall()
        for i in r:
            wallet= int(i[0])
            postId=i[1]
            query1="UPDATE post SET status=0 where id=?"
            cursor.execute(query1,(postId,))
        # Update data in db
        p="Accepted"
        wait="waitting"
        query="UPDATE bookrequest SET bookstatus=2,process=?,Waitprocess=?,WaittingValue=0 where reqId=?"
        cursor.execute(query,(p,wait,id,))
        db.commit()
        # Close db connection
        db.close()
        return redirect(url_for("notification"))

@app.route("/booksubmite")
def booksubmite():
    id=session["id"]
    con = sqlite3.connect('project.db')
    con.row_factory=sqlite3.Row
    c = con.cursor()  # cursor
    query = "SELECT * FROM user WHERE id=?"
    c.execute(query,(id,))
    rows1 = c.fetchall() 
    query = "SELECT * FROM bookrequest INNER JOIN user ON bookrequest.userId=user.id OR bookrequest.requserId=user.id INNER JOIN post ON bookrequest.postId=post.id WHERE user.id=?"
    c.execute(query,(id,))
    rows2 = c.fetchall() 
    return render_template("walletcon.html",rows1=rows1,rows2=rows2)

@app.route("/ignore/<int:id>")
def ignore(id):
    if session["login"]:
        db = sqlite3.connect('project.db')  
        cursor = db.cursor()
        query1="SELECT reqWallet,requserId FROM bookrequest WHERE reqId=?"
        cursor.execute(query1,(id,))
        r = cursor.fetchall()
        db.commit()
        for i in r:
            wallet= int(i[0])
            print(f" wallet: {wallet}")
            UserId=i[1]
        # Update data in db
        p="Cancel"
        query="UPDATE bookrequest SET bookstatus=0,process=? where reqId=?"
        cursor.execute(query,(p,id,))
        db.commit()
        query2="SELECT * FROM user WHERE id=?"
        # data for wallet back to request user
        cursor.execute(query2,(UserId,))
        r1 = cursor.fetchall()
        db.commit()
        for i in r1:
            value= int(i[4])
            result=value+wallet
            print(f"present value {result}")
            query="UPDATE user SET wallet=? where id=?"
            cursor.execute(query,(result,UserId,))
            db.commit()
        db.commit()
        # Close db connection
        db.close()
        return redirect(url_for("notification"))

@app.route("/submite/<int:id>",methods=['GET', 'POST'])
def submite(id):
    if request.method=="POST":
        file=request.files['file']
        image=file.filename
        token = request.form.get("token")
        file.save(os.path.join(app.config['UPLOAD_POST'], file.filename))
        path = (os.path.join(app.config['UPLOAD_POST'], file.filename))
        print(image)
        print(token)
        waitting = "ok"
        db = sqlite3.connect('project.db')
        c = db.cursor()
        query="UPDATE bookrequest SET Waitprocess=?,uTokenImage=?,token=?,WaittingValue=0 where reqId=?"
        c.execute(query,(waitting,image,token,id,))
        db.commit()
        db.close()
        return render_template("submit.html")
    return render_template("submit.html")
    

@app.route("/confirm/<int:id>",methods=['GET', 'POST'])
def confirm(id):
    msg=""
    if request.method=="POST":
        file=request.files['file']
        image=file.filename
        token = request.form.get("token")
        print(f"this token {token} ")
        file.save(os.path.join(app.config['UPLOAD_POST'], file.filename))
        path = (os.path.join(app.config['UPLOAD_POST'], file.filename))
        db = sqlite3.connect('project.db')
        c = db.cursor()
        query = "SELECT token,userId,reqWallet FROM bookrequest where reqId=?"
        c.execute(query,(id,))
        rows = c.fetchall() 
        for i in rows:
            print(i[0])
            if str(token) == str(i[0]):
                print("hello")
                userid=i[1]
                reqWallet=int(i[2])
                print(reqWallet)
                query = "SELECT wallet FROM user where id=?"
                c.execute(query,(userid,))
                rows1 = c.fetchall() 
                for j in rows1:
                    wallet=int(j[0])
                    result=reqWallet+wallet
                    print(f'result is {result}')
                    query="UPDATE user SET wallet=?  where id=?"
                    c.execute(query,(result,userid,))
                    db.commit()
            else:
                msg="wrong tokon"
                return render_template("submit.html",msg=msg)
        waitting = "ok"
        query="UPDATE bookrequest SET rTokenImage=?, WaittingValue=1 where reqId=?"
        c.execute(query,(image,id,))
        db.commit()
        db.close()
        msg="Tokon Submitted!"
        return render_template("submit.html",msg=msg)
    return render_template("submit.html")

@app.route("/history/<int:id>/")
def history(id):
    sid=session["id"]
    con = sqlite3.connect('project.db')
    con.row_factory=sqlite3.Row
    c = con.cursor()  # cursor
    query = "SELECT * FROM user WHERE id=?"
    c.execute(query,(sid,))
    rows1 = c.fetchall() 
    query = "SELECT * FROM bookrequest INNER JOIN user ON bookrequest.userId=user.id OR bookrequest.requserId=user.id INNER JOIN post ON bookrequest.postId=post.id WHERE bookrequest.reqId=?"
    c.execute(query,(id,))
    rows2 = c.fetchall() 
    return render_template("history.html",rows1=rows1,rows2=rows2)

@app.route("/bookhistory")
def bookhistory():
    con = sqlite3.connect('project.db')
    con.row_factory=sqlite3.Row
    c = con.cursor()  # cursor
    query = "SELECT * FROM bookrequest INNER JOIN user ON bookrequest.userId=user.id OR bookrequest.requserId=user.id INNER JOIN post ON bookrequest.postId=post.id"
    c.execute(query)
    rows = c.fetchall() 
    return render_template("bookSubAdmin.html",rows=rows)


@app.route("/profilepost")
def profilepost():
    if session["login"]:
        id=session["id"]
        con = sqlite3.connect('project.db')
        con.row_factory=sqlite3.Row
        c = con.cursor()  # cursor
        # read question : SQLite index startba from 1 (see index.html)
        query = "SELECT * FROM user WHERE id=?"
        c.execute(query,(id,))
        rows = c.fetchall()  # fetch the data from cursor
        query = "SELECT * FROM post WHERE userId=?"
        c.execute(query,(id,))
        rows1 = c.fetchall()
        con.commit()  # apply changes
        # go to thanks page : pass the value of tuple using question[0]
        con.close()
        return render_template("profilepost.html", rows=rows,rows1=rows1,id=id)

@app.route("/wallet")
def wallet():
    if session["login"]:
        id=session["id"]
        con = sqlite3.connect('project.db')
        con.row_factory=sqlite3.Row
        c = con.cursor()  # cursor
        query = "SELECT * FROM post INNER JOIN bookrequest ON post.id= bookrequest.postId where post.userId=? or requserId=?"
        c.execute(query,(id,id))
        rows = c.fetchall()  # fetch the data from cursor
        print(rows)
        query = "SELECT * FROM user WHERE id=?"
        c.execute(query,(id,))
        rows1 = c.fetchall()  # fetch the data from cursor
        print(rows1)
        query = "SELECT reqWallet,process FROM bookrequest WHERE requserId=?"
        c.execute(query,(id,))
        rows2 = c.fetchall()  
        for i in rows2:
            reqWallet=i[0]
            print(f"requetwallet is {reqWallet} ")
            process=i[1]
            if reqWallet==None:
                reqWallet=0
                process="nothing"
                return render_template("wallet.html",rows=rows,rows1=rows1,rows2=rows2,reqWallet=reqWallet,process=process)   
        query = "SELECT time FROM post INNER JOIN bookrequest ON post.id= bookrequest.postId where post.userId=? or requserId=?"
        c.execute(query,(id,id))
        rows = c.fetchall() 
        for i in rows:
            date=i[0]
        con.commit()  # apply changes
        con.close()
        return render_template("wallet.html",rows=rows,rows1=rows1,rows2=rows2,reqWallet=reqWallet,process=process)
    else:
        return redirect("/login")


@app.route("/review")
def review():
    con = sqlite3.connect('project.db')
    con.row_factory=sqlite3.Row
    c = con.cursor()  # cursor
    # read question : SQLite index startba from 1 (see index.html)
    query = "SELECT * FROM review"
    c.execute(query)
    rows = c.fetchall()  # fetch the data from cursor
    con.commit()  # apply changes
    con.close()
    rows.reverse()
    return render_template("review.html",rows=rows)


@app.route('/reviewpage/<int:id>')
def reviewpage(id):
    con = sqlite3.connect('project.db')
    con.row_factory=sqlite3.Row
    c = con.cursor()  # cursor
    query = "SELECT * FROM review WHERE reviewId=?"
    c.execute(query,(id,))
    rows = c.fetchall()  # fetch the data from cursor
    con.commit()  # apply changes
    con.close()
    return render_template("reviewpage.html",rows=rows)


@app.route("/")
def bookanimation():
    return render_template("bookanimation.html")

@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

@app.route("/addreview",methods=['GET', 'POST'])
def addreview():
    if session["login"]:
        con = sqlite3.connect('project.db')
        c = con.cursor() 
        if request.method=="POST":
            userid=session["id"]
            review = request.form.get("post")
            bookName = request.form.get("title")
            rating=request.form.get("prize")
            writer=request.form.get("writer")
            time=str(datetime.utcnow())
            file=request.files['file']
            image=file.filename
            file.save(os.path.join(app.config['UPLOAD_POST'], file.filename))
            path = (os.path.join(app.config['UPLOAD_POST'], file.filename))
            db = sqlite3.connect('project.db')
            c = db.cursor()
            c.execute("INSERT INTO review(userId, review, bookName, writer, ratting, image, date) VALUES (?,?,?,?,?,?,?)" , (userid, review,bookName,writer,rating,image,time))
            db.commit()
            db.close()
            return redirect("/review")
        con.row_factory=sqlite3.Row
        c = con.cursor()  # cursor
        query = "SELECT * FROM category"
        c.execute(query)
        rows = c.fetchall()  # fetch the data from cursor
        con.commit()  # apply changes
        con.close()
        return render_template("createreview.html")
    else:
        return redirect("/home")


@app.route("/admin")
def admin():
    return render_template("dashboard.html")



@app.route("/profile",methods=['GET', 'POST'])
def profile():
    if session["login"]:
        if request.method == 'POST':
            id=session["id"]
            file=request.files['file']
            image=file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            path = (os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            db = sqlite3.connect('project.db')  
            cursor = db.cursor()
            query="UPDATE user SET userimage=? where id=?"
            cursor.execute(query,(image,id,))
            db.commit()
            query1="SELECT * FROM user WHERE id=?"
            cursor.execute(query1,(id,))
            r= cursor.fetchall()
            db.close()
            return redirect("/profile")
        id=session["id"]
        con = sqlite3.connect('project.db')
        con.row_factory=sqlite3.Row
        c = con.cursor()  # cursor
        # read question : SQLite index startba from 1 (see index.html)
        query = "SELECT * FROM user where id=?"
        c.execute(query,(id,))
        rows = c.fetchall()  # fetch the data from cursor
        con.commit()  # apply changes
        con.close()
        return render_template("profile.html",rows=rows)
    else:
        redirect("/login")

@app.route("/adminlogin",methods=['GET', 'POST'])
def adminlogin():
    msg=""
    if request.method=="POST":
        name = request.form.get("name")
        password = request.form.get("password")
        db = sqlite3.connect('project.db')
        c = db.cursor()
        c.execute("SELECT * FROM admin WHERE name ='"+name+"' and password ='"+password+"'")
        r=c.fetchall()
        db.commit()
        db.close()
        for i in r:
            if i[0] == None:
                msg = "Wrong Username or password"
                return render_template("adminlogin.html", msg=msg)
            else:
                session["adminlogin"] = True
                session["adminid"] = i[0]
                session["adminname"] = name
                return redirect("/admin")
    return render_template("adminlogin.html", msg=msg)



#--------------Category Fuction-----------------------------
@app.route("/addcategory", methods=['GET', 'POST'])
def addcategory():
    if request.method=="POST":
        name = request.form.get("addcategory")
        icon = request.form.get("icon")
        db = sqlite3.connect('project.db')
        c = db.cursor()
        c.execute("INSERT INTO category(name, icon) VALUES (?,?)" , (name, icon))
        db.commit()
        db.close()
        return redirect("/admin")
    return render_template("addcategory.html")


@app.route("/categorytable")
def categorytable():
    con = sqlite3.connect('project.db')
    con.row_factory=sqlite3.Row
    c = con.cursor()  # cursor
    # read question : SQLite index startba from 1 (see index.html)
    query = "SELECT * FROM category"
    c.execute(query)
    rows = c.fetchall()  # fetch the data from cursor
    con.commit()  # apply changes
    con.close()
    return render_template("categorytable.html",rows=rows)

@app.route("/alluser")
def alluser():
    con = sqlite3.connect('project.db')
    con.row_factory=sqlite3.Row
    c = con.cursor()  # cursor
    # read question : SQLite index startba from 1 (see index.html)
    query = "SELECT * FROM user"
    c.execute(query)
    rows = c.fetchall()  # fetch the data from cursor
    con.commit()  # apply changes
    con.close()
    return render_template("alluser.html",rows=rows)

@app.route("/adminpage")
def adminpage():
    con = sqlite3.connect('project.db')
    con.row_factory=sqlite3.Row
    c = con.cursor()  # cursor
    # read question : SQLite index startba from 1 (see index.html)
    query = "SELECT * FROM user INNER JOIN post ON user.id=post.userId"
    c.execute(query)
    rows = c.fetchall()  # fetch the data from cursor
    con.commit()  # apply changes
    con.close()
    return render_template("page.html",rows=rows)

@app.route("/approve")
def approve():
    con = sqlite3.connect('project.db')
    con.row_factory=sqlite3.Row
    c = con.cursor()  # cursor
    # read question : SQLite index startba from 1 (see index.html)
    query = "SELECT * FROM user INNER JOIN post ON user.id=post.userId"
    c.execute(query)
    rows = c.fetchall()  # fetch the data from cursor
    con.commit()  # apply changes
    con.close()
    return render_template("approve.html",rows=rows)

@app.route("/userremove")
def userremove():
    con = sqlite3.connect('project.db')
    con.row_factory=sqlite3.Row
    c = con.cursor()  # cursor
    # read question : SQLite index startba from 1 (see index.html)
    query = "SELECT * FROM user"
    c.execute(query)
    rows = c.fetchall()  # fetch the data from cursor
    con.commit()  # apply changes
    con.close()
    return render_template("userremove.html",rows=rows)

@app.route('/userdelete/<int:id>')
def userdelete(id):
    # Connect to db
    print(id)
    db = sqlite3.connect('project.db')  
    cursor = db.cursor()
    # Update data in db
    cursor.execute("DELETE FROM user WHERE id=?",(id,))
    db.commit()
    # Close db connection
    db.close()
    return redirect(url_for("userremove"))


@app.route('/delete/<int:id>')
def delete(id):
    # Connect to db
    db = sqlite3.connect('project.db')  
    cursor = db.cursor()
    # Update data in db
    cursor.execute("DELETE FROM category WHERE id=?",(id,))
    db.commit()
    # Close db connection
    db.close()
    return redirect(url_for("categorytable"))



#---------------------Authentication-------------------------

@app.route("/reg", methods=['GET', 'POST'])
def reg():
    meg = ""
    if request.method=="POST":
        db = sqlite3.connect('project.db')
        c = db.cursor()
        c.execute("SELECT * FROM user")
        r = c.fetchall()
        user_first_name = request.form.get("first_name")
        username = request.form.get("username")
        user_email = request.form.get("email")
        user_password = request.form.get("password")
        for i in r:
            if i[6] == username or i[2] == user_email:
                if i[6] == username and i[2] == user_email:
                    meg = "Username and Email already here"
                elif i[6] == username and i[2] != user_email:
                    meg = "Username already here"
                else:
                    meg = "Email already here"
                return render_template("registration.html", meg=meg)
        wallet="500"
        userimage="shadow.png"
        mobile=request.form.get("mobile")
        location=request.form.get("location")
        db = sqlite3.connect('project.db')  
        c = db.cursor()
        c.execute("INSERT INTO user(name, email, password,wallet,userimage,username,mobile,lives) VALUES (?,?,?,?,?,?,?,?)" , (user_first_name, user_email,user_password,wallet,userimage,username,mobile,location))
        db.commit()
        db.close()
        return redirect("/login")
    return render_template("registration.html",meg=meg)



@app.route("/chome", methods=['GET', 'POST'])
def chome():
    msg=""
    if request.method=="POST":
        TranId = request.form.get("tranid")
        cid=session["cid"]
        print(cid)
        db = sqlite3.connect('project.db')
        c = db.cursor()
        query = "SELECT tranId,courierId FROM bookrequest WHERE courierId=? AND tranId=?"
        c.execute(query,(cid,TranId,))
        r=c.fetchall()
        print(r)
        for i in r:
            print(i[0])
            if i[0]==None:
              msg="Incorret Tran Id!"
              return render_template("subBook.html", msg=msg)  
        print("login")
        print(r)
        query="UPDATE bookrequest SET cStatus=1 where tranId=?"
        c.execute(query,(TranId,))
        db.commit()
        db.close()
        msg="succesfully book"
        return render_template("subBook.html", msg=msg)   
    return render_template("subBook.html", msg=msg)


@app.route("/login", methods=['GET', 'POST'])
def login():
    msg=""
    if request.method=="POST":
        name = request.form.get("username")
        password = request.form.get("userpassword")
        db = sqlite3.connect('project.db')
        c = db.cursor()
        c.execute("SELECT * FROM user WHERE username ='"+name+"' and password ='"+password+"'")
        r=c.fetchall()
        print("login")
        print(r)
        db.commit()
        db.close()
        for i in r:
            if i[0] == None:
                msg = "Wrong Username or password"
                return render_template("reg.html", msg=msg)
            else:
                session["login"] = True
                session["id"] = i[0]
                session["name"] = name
                session["Email"] = i[2]
                session["userimage"] = i[5]
                print("hello")
                print(session["id"])
                return redirect("/home")
    return render_template("reg.html", msg=msg)








@app.route("/logout")
def logout():
    session.pop('name', None)
    session.pop('login',False)
    session["login"]=False
    session.pop('id', None)
    login=0
    return redirect("/login")





# from app import app
if __name__=="__main__":
    app.run(debug=True)
