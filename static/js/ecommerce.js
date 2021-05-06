$(document).ready(function(){

  //contact form
  var contactForm = $('.contact-form')
  var contactFormEndPoint = contactForm.attr('action')
  var contactFormMethod = contactForm.attr('method')

  //dosubmit, will be assign later true or false, so that it will work on error and success
  function displaySpinning(submitBtn, defaultText, doSubmit){
    if(doSubmit){
      submitBtn.addClass('disabled')
      submitBtn.html('<i class="fa fa-spin fa-spinner"></i>Sending...')
    }else{
      submitBtn.removeClass("disabled")
      submitBtn.html(defaultText)
    }
  }

  contactForm.submit(function(event){
    event.preventDefault()
    //get that submit button
    var contactSubmitBtn = contactForm.find("[type='submit']")
    var contactSubmitBtnText = contactSubmitBtn.text()

    var contactData = contactForm.serialize()
    var thisForm = $(this)
    displaySpinning(contactSubmitBtn,"",true)

    $.ajax({
      url:contactFormEndPoint,
      method:contactFormMethod,
      data:contactData,

      success: function(data){
        thisForm[0].reset()
        $.alert({
          content:data.message
        })
        setTimeout(function(){
          displaySpinning(contactSubmitBtn,contactSubmitBtnText,false)
        },2000)
      },
      error: function(errorData){
        $.alert({
          content:"Error! form not submit"
        })
        setTimeout(function(){
          displaySpinning(contactSubmitBtn,contactSubmitBtnText,false)
        },2000)
      }
    })
  })

  //search via Jquery
  var searchForm = $('.search-form')
  var inputField = searchForm.find('[name=q]')
  var submitfield = searchForm.find('[type="submit"]')
  //need to be defined
  var typingTimer

  //same like submit function below for cart, keyup function means while typing key, something happens
  inputField.keyup(function(event){
    //when key is released
    clearTimeout(typingTimer)

    typingTimer = setTimeout(performSearch,1500)
  })

  inputField.keydown(function(event){
    //when key is pressed
    clearTimeout(typingTimer)
  })

  function performSearch(){
    submitfield.addClass('disabled')
    submitfield.html('<i class="fa fa-spin fa-spinner"></i>Searching...')
    var query = inputField.val()

    setTimeout(function(){
      window.location.href = '/search/?q=' + query
    },500)
  }


  //product and cart form
  var productForm = $('.form-product-ajax')

  productForm.submit(function(event){
    event.preventDefault();
    console.log('form not sending')
    formData = $(this)

    var actionEndPoint = formData.attr('data-endpoint');
    var httpMethod = formData.attr('method');
    var productData = formData.serialize();

    $.ajax({
      url:actionEndPoint,
      method:httpMethod,
      data:productData,

      success: function(data){
        console.log('data succesfully sent')
        if(data.added){
          productForm.find('.submit-span').html('In Cart<button type="submit" class="btn btn-link">Remove</button>')
          console.log('Added: ', data.added)
        }else{
          productForm.find('.submit-span').html('<button type="submit" class="btn btn-link">Add To Cart</button>')
          console.log('Removed: ', data.removed)
        }
        var productCountDisplay = $('.cart-product-count')
        //change the text display using text() and sending the json data
        productCountDisplay.text(data.cartProductCount)

        //if remove is clicked from cart homepage, then only we refresh the cart
        var currentPath = window.location.href
        if(currentPath.indexOf('cart') != -1){
          refreshCart()
        }
      },
      error: function(errorData){
        console.log('data sent unsuccesfull')
      }
    })
  })

  //we create refresh cart function here, as it only runs after removed is clicked from cart homepage, so all previous removing of product and changing button to add to cart works in product detail page, after that it refresh the homepage
  function refreshCart(){
    var table = $('.cart-table')
    var tableBody = table.find('.cart-body')
    var tableRow = tableBody.find('.cart-product')

    var refreshCartUrl = '/api/cart/'
    var refreshCartMethod = 'GET'
    var data = {}

    $.ajax({

      url:refreshCartUrl,
      method:refreshCartMethod,
      data:data,

      success: function(data){
        console.log('data sent success')

        var hiddenRemoveForm = $('.cart-item-remove-form')

        if(data.product.length > 0){
          //not understodo but mandatory
          tableRow.html(' ')

          i = data.product.length
          $.each(data.product,function(index,value){
            //on every loop we create that removebutton with different id in hidden input type
            var newHiddenRemoveForm = hiddenRemoveForm.clone()
            //displaying the form button
            newHiddenRemoveForm.css('display','block')
            //setting value to hidden input product id, so that when remove is clicked, it performs normal on the basis of id
            newHiddenRemoveForm.find('.cart-item-product-id').val(value.id)
            //add table rows in the body
            tableBody.prepend("<tr><th scope=\"row\">" + i + "</th><td><a href='" + value.url + "'>" + value.name + "<a/>" + newHiddenRemoveForm.html() + "</td><td>" + value.price + "</td></tr>" )

            i--
          })
        }else{
          //if product is 0, then refresh the page
          window.location.href = window.location.href
        }

      },
      error:function(errorData){
        console.log('Error')
      }

    })
  }

})
