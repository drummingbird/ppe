/*
 *    This program is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU Affero General Public License as
 *    published by the Free Software Foundation, either version 3 of the
 *    License, or (at your option) any later version.
 *
 *    This program is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU Affero General Public License for more details.
 *
 *    You should have received a copy of the GNU Affero General Public License
 *    along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

/*
 * This file is intended to add interactivity to assignment forms.
 */

$(document).ready(function () {
    'use strict';

    console.debug("[mqo_exercise] Custom JS for assignments is loading...");

    var the_form = $('.js_responseform');
    var submit_controller = the_form.attr("data-submit");

    // Parameters for form submission
    $('.js_responseform').ajaxForm({
        url: submit_controller,
        type: 'POST',                       // submission type
        dataType: 'json',                   // answer expected type
        beforeSubmit: function(){           // hide previous errmsg before resubmitting
        },
        success: function(response, status, xhr, wfe){ // submission attempt
            if(_.has(response, 'errors')){  // some questions have errors
                _.each(_.keys(response.errors), function(key){
                });
                return false;
            }
            else if (_.has(response, 'reply')){      // form is ok and we got a response
                $("#ex_response").html(response.reply);
                return true;
            }
            else if (_.has(response, 'redirect')){      // form is ok
                window.location.replace(response.redirect);
                return true;
            }
            else {                                      // server sends bad data
                console.error("Incorrect answer sent by server");
                return false;
            }
        },
        timeout: 5000,
        error: function(jqXHR, textStatus, errorThrown){ // failure of AJAX request
            $('#AJAXErrorModal').modal('show');
        }
    });

    console.debug("[mqo_exercise] Custom JS for assignments loaded!");
});
