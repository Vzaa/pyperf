function do_action(url)
{
    $.ajax({
        url: url,
        dataType: 'json',
        success: function(data){
            //console.log('success');
            //console.log(data);
            //console.log(url);
            //timer = setTimeout('fill_stuff()', 200);
        },
        error: function(  jqXHR, textStatus,  errorThrown ) {
            console.log(errorThrown);
        }
    });
}


function plot_item(id_no, list)
{
    console.log(list.tput);
    $.plot("#placeholder"+id_no, [  list.tput ]);
    if (list.running) {
        setTimeout(function() { plot_item_json(id_no)}, 1000);
    }
}

function plot_item_json(id_no)
{
    $.ajax({
        url: '/get_parsed?id_no=' + id_no,
        dataType: 'json',
        success: function(data) {
            plot_item(id_no, data);
        },
        error: function( data ) {
            console.log(data);
        }
    });
}
