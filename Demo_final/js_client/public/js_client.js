
/**
 * A small function which calls the server to execute a batch job
 */
async function do_job(){

  $('#preview').attr("src", "https://media1.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif")

  var job_data = get_job_data();
  console.log(job_data);
  $.ajax({
            type: "POST",
            url: "http://localhost:5000",
            data: JSON.stringify(job_data),
            dataType: 'json',
            headers: {"Content-Type": "application/json"},
            statusCode:{
              200: function(){
                //Loads preview picture may be a bit buggy
                $('#preview').attr("src", "./data/nc_preview.png");
              }
            }
        });
} 

/**
 * Function which takes the job data from the from node in the HTML 
 */
function get_job_data(){
  var process     = $('#process').val(),
      title       = $('#title').val(),
      description = $('#description').val(),
      start = $('#start').val(),
      end = $('#end').val()
      //bbox =$('#bbox').val();

  console.log(process, title, description, start, end)

  var validate_arr = [process, title, description, start, end]

  for(x in validate_arr){
    if(validate_arr[x] == ""){
      throw new Error('Alle Felder müssen ausfgefüllt werden.'); 
    }
  }

  calc_ndvi  = {
    'process_id': "ndvi",
    'arguments': {
      'data':{
          'from_node': 'loadcollection1'
      },
      'bb' : [-999,-999,-999,-999]
      }
  };

  calc_sst  = {
    'process_id': "mean_sst",
    'arguments': {
      'data':{
          'from_node': 'loadcollection1'
      },
      'timeframe':[start ,end],
      'bbox' : [-999,-999,-999,-999]
      }
  };

  var job_data= { 
    'title': title,
    'description': description, 
    'process_graph': {
      'loadcollection1': {
        'process_id': 'load_collection',
        'arguments': {
          'timeframe' : [ (date_conversion(start) + ' 00:00:00'),(date_conversion(end) + ' 00:00:00'),'%d-%m-%Y %H:%M:%S'],
          'DataType': ((process == 'sst') ? "SST" : "Sentinel2")
          }
        },
        'calculation': ((process == 'sst') ? calc_sst : calc_ndvi),
        'save':{
            'process_id': 'save_result',
            'arguments':{
                'SaveData':{
                    'from_node':'calculation'
                },
                'Format': 'netcdf'
            }
        }
    }
  }

  return job_data
}

/**
 * Small date converison function
 * @param {string} date 
 */
function date_conversion(date){
  new_date = date.substring(8) + '-' + date.substring(5,7) +  '-' + date.substring(0,4)
  return new_date;
}