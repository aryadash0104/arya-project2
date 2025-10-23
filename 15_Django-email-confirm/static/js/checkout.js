$(document).ready(function () {
    $('.paywithRazorPay').click(function (e) {
        e.preventDefault();
        var token = $("[name='csrfmiddlewaretoken']").val();
        var imageIds = [];  // Array to store the IDs of selected images

        // Iterate over each selected image and push its ID to the array
        $('.checkout__total__products li').each(function () {
            var imageId = $(this).data('imageid');
            if (imageId) {
                imageIds.push(imageId);
            }
        });


        $.ajax({
            method: "GET",
            url: "/profiles/proceed-to-pay/",
            success: function (response){
                // console.log(response)
                var options = {
                    "key": "rzp_test_MP1ouUpRe69TNK", // Enter the Key ID generated from the Dashboard
                    "amount": 1*100,//response.total_price * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                    "currency": "INR",
                    "name": "InstHello", //your business name
                    "description": "Purchasing The Image, Thank You",
                    "image": "https://example.com/your_logo",
                    "handler": function (responseb){
                        alert(responseb.razorpay_payment_id);                        
                        data = {
                            "name":checkoutData.name,
                            "email": checkoutData.email,
                            "contact": checkoutData.contact,
                            "image_ids": imageIds, 
                            csrfmiddlewaretoken: token,
                        }
                        $.ajax({
                            method: "POST",
                            url: "/profiles/place-order/",
                            data: data,
                            success: function (response){
                                alert("Order Placed Successfully");
                            },
                            error: function (xhr, status, error) {
                                console.error(xhr.responseText);
                                var errorMessage = "Failed to place order. Please try again.";
                                if (xhr.responseJSON && xhr.responseJSON.error) {
                                    errorMessage = xhr.responseJSON.error;
                                }
                                alert(errorMessage);
                            }
                        });
                    },
                    "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information, especially their phone number
                        "name": checkoutData.name, //your customer's name
                        "email": checkoutData.email, 
                        "contact": checkoutData.contact  //Provide the customer's phone number for better conversion rates 
                    },
                    "theme": {
                        "color": "#3399cc"
                    }
                };
                var rzp1 = new Razorpay(options);
                
                rzp1.open();
            }
        })     
    })
});