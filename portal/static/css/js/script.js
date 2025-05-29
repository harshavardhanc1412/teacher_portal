$(document).ready(function() {
    // Add new student
    $('#saveStudent').click(function() {
        const name = $('#name').val();
        const subject = $('#subject').val();
        const marks = $('#marks').val();
        
        if (name && subject && marks) {
            $.ajax({
                url: '/manage-student/',
                type: 'POST',
                data: JSON.stringify({
                    action: 'add',
                    name: name,
                    subject: subject,
                    marks: marks
                }),
                contentType: 'application/json',
                headers: {
                    'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(response) {
                    if (response.status === 'success') {
                        location.reload();
                    }
                },
                error: function(xhr) {
                    alert('Error adding student: ' + xhr.responseJSON.message);
                }
            });
        } else {
            alert('Please fill all fields');
        }
    });
    
    // Edit student inline
    $('.editable').click(function() {
        const cell = $(this);
        const originalValue = cell.text().trim();
        const field = cell.data('field');
        const row = cell.closest('tr');
        const studentId = row.data('id');
        
        cell.html(`<input type="${field === 'marks' ? 'number' : 'text'}" 
                         class="form-control form-control-sm" 
                         value="${originalValue}">`);
        
        const input = cell.find('input');
        input.focus();
        
        input.blur(function() {
            const newValue = input.val().trim();
            if (newValue !== originalValue) {
                $.ajax({
                    url: '/manage-student/',
                    type: 'POST',
                    data: JSON.stringify({
                        action: 'edit',
                        id: studentId,
                        name: field === 'name' ? newValue : row.find('[data-field=name]').text().trim(),
                        subject: field === 'subject' ? newValue : row.find('[data-field=subject]').text().trim(),
                        marks: field === 'marks' ? newValue : row.find('[data-field=marks]').text().trim()
                    }),
                    contentType: 'application/json',
                    headers: {
                        'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
                    },
                    success: function(response) {
                        if (response.status === 'success') {
                            cell.text(newValue);
                        }
                    },
                    error: function(xhr) {
                        alert('Error updating student: ' + xhr.responseJSON.message);
                        cell.text(originalValue);
                    }
                });
            } else {
                cell.text(originalValue);
            }
        });
        
        input.keypress(function(e) {
            if (e.which === 13) { // Enter key
                input.blur();
            }
        });
    });
    
    // Delete student
    $('.delete-btn').click(function() {
        if (confirm('Are you sure you want to delete this student?')) {
            const row = $(this).closest('tr');
            const studentId = row.data('id');
            
            $.ajax({
                url: '/manage-student/',
                type: 'POST',
                data: JSON.stringify({
                    action: 'delete',
                    id: studentId
                }),
                contentType: 'application/json',
                headers: {
                    'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(response) {
                    if (response.status === 'success') {
                        row.remove();
                    }
                },
                error: function(xhr) {
                    alert('Error deleting student: ' + xhr.responseJSON.message);
                }
            });
        }
    });
    
    // Reset modal on close
    $('#studentModal').on('hidden.bs.modal', function() {
        $('#studentForm')[0].reset();
    });
});