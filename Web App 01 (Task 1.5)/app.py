from flask import Flask, render_template, url_for, redirect, request
import sqlite3

app = Flask(__name__)


@app.route('/')
def home():
    return "My Homepage."


@app.route('/search/', methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")

    else:
        team_no = request.form['team_no']

        query1 = """
        SELECT agents.Name, agents.BaseSalary
        FROM agents
        WHERE TeamNo = ?
        """

        db = sqlite3.connect('Tutorial web app 01 (Task 1.2).db')
        cursor = db.execute(query1, (team_no,))
        data1 = cursor.fetchall()
        cursor.close()
        db.close()


        query2 = """
        SELECT agents.Name, policyrecords.PolicyID, policyrecords.StartDate
        FROM agents, policyrecords, policies
        WHERE policyrecords.StartDate >= 20200101 AND policyrecords.StartDate <= 20200401 AND agents.AgentID = policyrecords.AgentID AND policyrecords.PolicyID = policies.PolicyID AND TeamNo = ?
        ORDER BY policyrecords.StartDate ASC
        """

        db = sqlite3.connect('Tutorial web app 01 (Task 1.2).db')
        cursor = db.execute(query2, (team_no,))
        data2 = cursor.fetchall()
        cursor.close()
        db.close()

        commission = [3760, 2100, 450, 2700, 1500, 960, 3487.5, 4140, 2940, 7200]
        policy = ['POL001', 'POL002', 'POL003', 'POL004', 'POL005', 'POL006', 'POL007', 'POL008', 'POL009', 'POL010']
        
        agents = []
        base_salary = []
        for row in data1:
            agents.append(row[0])
            base_salary.append(row[1])

        jan = []
        feb = []
        mar = []

        for line in data2:
            if line[2] < 20200201:
               jan.append(line)
            elif line[2] < 20200301:
                feb.append(line)
            else:
                mar.append(line)

        for i in range(len(jan)):
            for agent in agents:
                if jan[i][0] == agent:
                    jan[i] += (agents.index(agent),)

            jan[i] += (base_salary[jan[i][3]],)

            for pol in policy:
                if jan[i][1] == pol:
                    jan[i] += (commission[policy.index(pol)],)

        for i in range(len(feb)):
            for agent in agents:
                if feb[i][0] == agent:
                    feb[i] += (agents.index(agent),)

            feb[i] += (base_salary[feb[i][3]],)

            for pol in policy:
                if feb[i][1] == pol:
                    feb[i] += (commission[policy.index(pol)],)

        for i in range(len(mar)):
            for agent in agents:
                if mar[i][0] == agent:
                    mar[i] += (agents.index(agent),)

            mar[i] += (base_salary[mar[i][3]],)

            for pol in policy:
                if mar[i][1] == pol:
                    mar[i] += (commission[policy.index(pol)],)        
            

            for agent in agents:
                check = False

                for i in range(len(jan)):
                    if jan[i][0] == agent:
                        check = True
                
                if check == False:
                    jan.append((agent, 0, 0, 0, base_salary[agents.index(agent)], 0))


            for agent in agents:
                check = False

                for i in range(len(feb)):
                    if feb[i][0] == agent:
                        check = True
                
                if check == False:
                    feb.append((agent, 0, 0, 0, base_salary[agents.index(agent)], 0))

            for agent in agents:
                check = False

                for i in range(len(mar)):
                    if mar[i][0] == agent:
                        check = True
                
                if check == False:
                    mar.append((agent, 0, 0, 0, base_salary[agents.index(agent)], 0))



        fin_jan = []
        fin_feb = []
        fin_mar = []

        for agent in agents:
            count = 0
            agent_index = []
            for i in range(len(jan)):
                if agent == jan[i][0]:
                    count += 1
                    agent_index.append(i)

            if count == 1:
                total = jan[agent_index[0]][4] + jan[agent_index[0]][5]
                fin_jan.append((agent, total))
            else:
                total = jan[agent_index[0]][4] + jan[agent_index[0]][5]

                for i in range(1, len(agent_index)):
                    total += jan[agent_index[i]][5]

                    fin_jan.append((agent, total))

        for agent in agents:
            count = 0
            agent_index = []
            for i in range(len(feb)):
                if agent == feb[i][0]:
                    count += 1
                    agent_index.append(i)

            if count == 1:
                total = feb[agent_index[0]][4] + feb[agent_index[0]][5]
                fin_feb.append((agent, total))
            else:
                total = feb[agent_index[0]][4] + feb[agent_index[0]][5]

                for i in range(1, len(agent_index)):
                    total += feb[agent_index[i]][5]

                    fin_feb.append((agent, total))

        for agent in agents:
            count = 0
            agent_index = []
            for i in range(len(mar)):
                if agent == mar[i][0]:
                    count += 1
                    agent_index.append(i)

            if count == 1:
                total = mar[agent_index[0]][4] + mar[agent_index[0]][5]
                fin_mar.append((agent, total))
            else:
                total = mar[agent_index[0]][4] + mar[agent_index[0]][5]

                for i in range(1, len(agent_index)):
                    total += mar[agent_index[i]][5]

                    fin_mar.append((agent, total))

        pay = []
        for i in range(len(fin_jan)):
            pay.append((fin_jan[i][0], "{:.2f}".format(fin_jan[i][1]), "{:.2f}".format(fin_feb[i][1]), "{:.2f}".format(fin_mar[i][1])))
            

        return render_template("display.html", pay=pay)


if __name__ == "__main__":
    app.run(debug=True)
