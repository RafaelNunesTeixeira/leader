    let bidBtn = document.getElementById('btn-bid');
    let msgMyStatus = document.getElementById('msg-my-status');
    let msgMyBid = document.getElementById('msg-my-bid');





    function sendBid(btn){
        if (bidBtn.checked == true){
             msgMyStatus.innerText = 'You are waiting for a group:';

             liveSend(parseInt(2));}

        if (bidBtn.checked == false){
            msgMyStatus.innerText = 'Check the box below to search for a group:';
            liveSend(parseInt(1));}
    }

    function liveRecv(data) {
        console.log('liveRecv', data);
        let myid = js_vars.my_id;
        let tamanho = js_vars.tamanho;

        if (data.top_bid === 0) {
            msgMyBid.innerText = `Nobody is waiting for the experiment`;
         }
        if (data.top_bid === 1) {
            msgMyBid.innerText = '1 is waiting for the experiment';
         }
         if (data.top_bid === 3) {
            msgMyBid.innerText = '2 are waiting for the experiment';
         }
         if (data.top_bid === 2) {
            msgMyBid.innerText = ` ${data.top_bid} are waiting for the experiment `;
         }
    }



    document.addEventListener("DOMContentLoaded", function (event) {
        liveSend({});
    });

