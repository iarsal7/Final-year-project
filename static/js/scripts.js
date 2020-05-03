


    // $(document).ready(function(){
    //     var productForm = $(".form-update-ajax") //remove from cart
    //     productForm.submit(function(event){
    //     event.preventDefault();
    //     var thisForm = $(this)
    //     var action= thisForm.attr("action");
    //     var method = thisForm.attr("method");
    //     var formData = thisForm.serialize();

    //   $.ajax({
    //     url: action,
    //     method: method,
    //     data: formData,
    //     success: function(data){
        
    //     var cartcount= $(".cart-count") //cart-count is span field in base.html
    //     cartcount.text(data.cartCount) //cartCount is jsonResponse in views

    //     var path= window.location.href
    //     if (path.indexOf("cart") != -1){
    //       CartUpdate()
    //     }

    //     },

    //   error: function(errorData){
    //     console.log("error")
    //     console.log(errorData)
    //                              }
    //   }) //ajax closing

    //     }) //form submit end

    //   function CartUpdate(){

    //     var action= '/api/cart/'
    //     var method= "GET"; 
    //     var formData= {};
    //     var table= $(".cart-table")
    //     var body= table.find(".cart-body")
    //     var row = body.find(".cart-product")
    //     var cartheading= table.find(".cartheading")
    //     var removeForm = $(".cart-remove-form")

    //     $.ajax({

    //       url: action,
    //       method: method,
    //       data: formData,

    //       success:function(data){
    //         console.log(data)
    //         if (data.cart.length > 0){
    //           row.html("")
    //           k=data.cart.length

    //           $.each(data.cart ,function(index , value){  
    //             var removeform = removeForm.clone()

    //             removeform.css("display" , "block")
    //            // removeform.removeClass("class name") //in case if we use class in cart update form
    //             removeform.find(".cartproduct").val(value.id)

    //             body.prepend("<tr><th scope=\"row\">" + k + " </th><td> "+ value.title +" " +removeform.html() +" </td> <td> " + value.quantity
    //              + " </td> <td> " + value.price + "</td> <td> " + value.total + "</td> </tr>")
                
    //             k--
    //           })
              
    //         }

    //         else{
    //         cartheading.css("display", "none")
    //         body.html("")
    //         body.html("<h1>Cart empty</h1>")
             
    //          }
    //       },

    //       error: function(errorData){
    //         console.log("error")
    //         console.log(errorData)
    //       }

    //     }) // ajax call inside function cart update

    //   } //function cart update ending

    //   })

  