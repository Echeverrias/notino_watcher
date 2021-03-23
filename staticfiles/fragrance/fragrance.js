$(document).ready(function(){

    console.log("LOADING JQUERY")

     const getToken = () => {
        console.log('getToken')
        console.log('token: ', $('input[name="csrfmiddlewaretoken"]').val())
        return $('input[name="csrfmiddlewaretoken"]').val()
    }

    const getTokenData = () => {
        return {csrfmiddlewaretoken: getToken()}
    }

    const delete_fragrance = (e) => {
            e.preventDefault();
            console.log('button has been clicked');
            console.log(e);
            let button = e.target
            url = button.getAttribute('data-url')
            console.log(url)
            data = getTokenData()
            $.ajax({
                type: 'POST',
                url: url,
                data: data,
                success: e => {
                    console.log(e.message);
                    button.parentElement.remove();
                    display_msg('#url_form_result', e.error?e.error:e.message, 'p', e.error?'error':'')
                },
                error: e => {
                    let msg = get_msg_error(e)
                    display_msg('#url_form_result', msg, 'p', 'error')
                }
            })
            return false
           }

     try{

        $('#url_form').on('submit', (e) => {
            e.preventDefault();
            e.stopImmediatePropagation();
            console.log('submit5');
            console.log(e);
            let form = e.target
            let url = form['url'].value
            let token = form['csrfmiddlewaretoken'].value
            let data = {csrfmiddlewaretoken: token, url:url}
            let formData = new FormData(form);
            let queryString = new URLSearchParams(formData).toString();
            type = form.method
            url = form.action
            //save_url(type, url, data)
            save_url(type, url, queryString)
        })

         $('button.delete').off('click').on('click', delete_fragrance)

    }
     catch(e){
        console.error(e);
    }


    function get_msg_error(error){
        console.log(error)
        if (error?.status === 500){
            return 'Error: Se ha producido un error en el servidor';
        }
        else if (error?.status === 0){
            return 'Error: La conexión ha sido rechazada', 'h4', 'title alert alert-danger';
        }
        else{
            return 'Error';
        }
    }

    function handle_error(error){
        console.log(error);
        err = get_msg_error(error);
        if (error.status === 500){
            display_msg(err, 'h4', 'title alert alert-danger');
        }
        else if (error.status === 0){
            display_msg(err, 'h4', 'title alert alert-danger');
        }
        else{
            display_msg(err, 'h4', 'title alert alert-danger');
        }
    }

    function display_msg(queryDestiny, msg, tag, classes){
        //alert(msg);
        html = `<${tag} class="${classes}">  ${msg}  </${tag}>` ;
        $(queryDestiny).html(html);
    }

    function save_url(type, url, data){
       console.log('Ajax save-url request');
       $.ajax({
            type: type,
            url: url,
            data: data,
            success: e => {
                console.log(e)
                console.log(e.message)
                display_msg('#url_form_result', e.error?e.error:e.message, 'p', e.error?'error':'')
                if (e.error) return false
                let fragrance = e.fragrance
                fragrance_str = `${fragrance.brand} ${fragrance.name} Eau de ${fragrance.type} pour ${fragrance.gender} ${fragrance.size}ml ${fragrance.price}€ ${fragrance.is_in_offer? "is in offer ":""}(${fragrance.max_offer_price}€-${fragrance.min_offer_price}€, ${fragrance.min_price}€-${fragrance.max_price}€)`
                let button = $(`<button class="delete" data-url="/fragrances/delete/${fragrance.pk}/" class="delete-fragrance">X</button>`)
                button.on('click', delete_fragrance)
                $('ul.list li:first').before(`<li><a href="${fragrance.url}">${fragrance_str}</a></li>`)
                $('ul.list li:first').append(button)
                //$('ul.list').append($("<li>").html(`<a href="${fragrance.url}">${fragrance}</a>`))
                /*
                    let a = document.createElement('a')
                    a.href = fragrance.url
                    a.appendChild(document.createTextNode(fragrance_str))
                    let li = document.createElement('li')
                    li.appendChild(a)
                    let ul = document.querySelector('ul.list')
                    ul.appendChild(li)
                */
                $('#url').val('');
            },
            error: e => {
                let msg = get_msg_error(e)
                 alert(`error: ${msg}`)
                display_msg('#url_form_result', msg, 'p', 'error')
            }
        })
        return false
    }


    function set_attribute(element, attribute, value){
        try{
            element.attr(attribute, value);
        }
        catch(e){
              try{
                element.attr(attribute, value);
                element[attribute] = value
              }
            catch(e){
                console.error(e);
            }
        }
    }

    function get_attribute(element, attribute){
        try{
            return element.attr(attribute);
        }
        catch(e){
              try{
                return element.getAttribute(attribute);
              }
            catch(e){
                console.error(e)
                return undefined
            }
        }
    }



})