//Loading modules 
const express = require('express');
const { OpenEO } = require('@openeo/js-client');
const { JSDOM } = require( "jsdom" );
const { window } = new JSDOM( "" );
const $ = require( "jquery" )( window );
const fs = require('fs');
const path = require('path');
const {spawn} = require('child_process');

//express Setup
const app     = express();
const port    = 5000;

app.use(express.json());

//File usage for express
app.use('/public', express.static(__dirname +'/public'));
app.use('/data', express.static(__dirname +'/data'));

//Show index HTML at localhost:5000
app.get('/',
         (req,res) => res.sendFile(__dirname + '/js_client.html')
);

app.post('/', (
    async (req,res) => {
        console.log(req.body)
        job_data = req.body

        try {
            //Creation of the connection
            var con = await OpenEO.connect("http://localhost/api/v1");

            //Creation and start of new job 
            new_job = await con.createJob(job_data.process_graph, job_data.title, job_data.description);     
            await new_job.startJob();

            //Monitoring of the job with callback function when finished
            new_job.monitorJob(async(new_job, logs) => {
                if (new_job.status === "finished") {

                    //Download of the results 
                    await new_job.downloadResults('./data');

                    //Converision to netcdf file 
                    results = await new_job.listResults();
                    var filename = results[0].href;
                    filename = filename.substring(filename.length - 36 );
                    fs.renameSync(path.join(__dirname, 'data',  filename) , path.join(__dirname, 'data',  filename + '.nc'));

                    //Start python script to make preview picture
                    const python = spawn('python', ['convert_to_png.py', job_data.process_graph.calculation.process_id]);
                    python.on('close', (code) =>{ 
                        console.log(`child process close all stdio with code ${code}`)
                        //Send response
                        res.send('Finished');
                    });

                    
                }
            }, 5);
        } catch (error) {
            console.log(error);
        }
    })
);

app.listen(port,
    () => console.log('JS client demo app listening at http://localhost:'+port));