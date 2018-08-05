
$(document).ready(function ready(){
   $('#uploadHandler').click(function(e) {
       // console.log(e);
       // console.log($(this));
       let files = $('#file-upload').prop('files');
       e.preventDefault();
       // console.log($('.subform')[0][0].files[0])
       let data = new FormData();
       data.append("uploadFile", files[0]);
       data.append("key", $('#key').val());
       data.append("name", $('#name').val());
       console.log(data);
       $.ajax({
           url: '/upload',
           type: 'POST',
           data: data,
           cache: false,
           processData: false,
           contentType: false,
           timeout: 3000,
           success: function successHandler(data, textStatus) {
               if (data.state === 0) {
                   $('#upLoadedStatus').html(`上传成功，URL为：${data.url}`);
               }
               else if (data.state === 1) {
                   $('#upLoadedStatus').html(`上传失败，key不正确`);
               }
               else if (data.state === 2) {
                   $('#upLoadedStatus').html(`上传失败，文件名不正确，只能是字母开头，包含字母和数字`);
               }
               else if (data.state === 3) {
                   $('#upLoadedStatus').html(`上传失败，不明错误`);
               }
           },
           error: function errorHandler(xhr, textStatus, errorThrown) {
               $('#upLoadedStatus').html(`上传失败，服务器错误`);
           }
       })
   })
});
