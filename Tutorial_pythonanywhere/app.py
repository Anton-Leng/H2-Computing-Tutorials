from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/about/')
def about():
    return render_template("about.html")


@app.route('/rp_calc/', methods=["GET", "POST"])
def rp_calc():
    if request.method == "GET":
        return render_template("calc.html")
    else:
        pw, mt = request.form.get("pw"), request.form.get("mt")
        return render_template("calc2.html", pw=pw, mt=mt)


@app.route('/calc2/', methods=["GET", "POST"])
def rp_calc2():
    return render_template("calc2.html")


@app.route('/calc3/', methods=["GET", "POST"])
def rp_calc3():
    if request.method == "GET":
        return render_template("calc3.html")
    else:
        h1 = [10, 8.75, 7.5, 6.25, 5, 2.5, 0, 0]
        h2 = [20, 17.5, 15, 12.5, 10, 5, 0, 0]
        grade = ["A", "B", "C", "D", "E", "S", "U", None]
        h2s1g, h2s2g, h2s3g, h1g, GPg, PWg, MTg = request.form.get("h2s1g"), request.form.get("h2s2g"), request.form.get("h2s3g"), request.form.get("h1g"), request.form.get("GPg"), request.form.get("PWg"), request.form.get("MTg")
        h2s1gi, h2s2gi, h2s3gi, h1gi, GPgi, PWgi, MTgi = grade.index(request.form.get("h2s1g")), grade.index(request.form.get("h2s2g")), grade.index(request.form.get("h2s3g")), grade.index(request.form.get("h1g")), grade.index(request.form.get("GPg")), grade.index(request.form.get("PWg")), grade.index(request.form.get("MTg"))
        pw, mt = request.form.get("pw"), request.form.get("mt")

        h2s1p, h2s2p, h2s3p = h2[h2s1gi], h2[h2s2gi], h2[h2s3gi]
        h1p, GPp, PWp, MTp = h1[h1gi], h1[GPgi], h1[PWgi], h1[MTgi]
        base_sum = h2s1p + h2s2p + h2s3p + h1p + GPp
        total = 0

        if pw == "no" and mt == "no":
            total += base_sum
        if pw == "yes" and mt == "no":
            total += (base_sum + PWp)
        if pw == "no" and mt == "yes":
            if (((base_sum + MTp)/90) * 80) >= base_sum:
                total += (((base_sum + MTp)/90) * 80)
            else:
                total += base_sum
        if pw == "yes" and mt == "yes":
            if (((base_sum + MTp + PWp)/100) * 90) >= (base_sum + PWp):
                total += (((base_sum + MTp + PWp)/100) * 90)
            else:
                total += (base_sum + PWp)

        total = '{:.2f}'.format(total)
        return render_template("calc3.html", h2s1g=h2s1g, h2s2g=h2s2g, h2s3g=h2s3g, h1g=h1g, GPg=GPg, PWg=PWg, MTg=MTg, total=total, pw=pw, mt=mt, h2s1p=h2s1p, h2s2p=h2s2p, h2s3p=h2s3p, h1p=h1p, GPp=GPp, PWp=PWp, MTp=MTp)


if __name__ == "__main__":
    app.run(debug=True)
