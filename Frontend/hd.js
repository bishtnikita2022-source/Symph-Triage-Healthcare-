async function analyzeDisease(){

    let symptoms = document
        .getElementById("symptoms")
        .value
        .toLowerCase()
        .split(",")
        .map(s => s.trim());

    let duration = parseInt(
        document.getElementById("duration").value
    );

    let severity =
        document.getElementById("severity").value;

    if(symptoms.length === 0 || !duration){

        alert("Enter all fields");

        return;
    }

    try{

        const response = await fetch(
            "http://127.0.0.1:5000/analyze",
            {
                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({
                    symptoms,
                    duration,
                    severity
                })
            }
        );

        const data = await response.json();

        let html = `<h2>Results</h2><br>`;

        let maxScore =
            data.ranked[0].score || 1;

        data.ranked.forEach((d,index)=>{

            let percent =
                (d.score/maxScore)*100;

            html += `

            <div class="disease">

                <div class="${index===0 ? 'top':''}">
                    ${d.disease}
                    (Score: ${d.score})
                </div>

                <div class="bar">

                    <div class="fill"
                        style="width:${percent}%">
                    </div>

                </div>

            </div>
            `;
        });

        html += `
        <p>
        <b>Urgency:</b>
        ${data.urgency}
        </p>
        `;

        html += `
        <br>

        <p>
        <b>Suggested Tests:</b>
        ${data.tests.join(", ")}
        </p>
        `;

        document
            .getElementById("result")
            .innerHTML = html;

    }
    catch(error){

        console.log(error);

        document
            .getElementById("result")
            .innerHTML =
            "Server Error";
    }
}