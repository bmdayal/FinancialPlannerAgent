$(document).ready(function() {
    // Chat UI elements
    const chatbox = $('#chatbox');
    const chatToggle = $('#chatToggle');
    const chatMessages = $('.chat-messages');
    const chatInput = $('#chatInput');
    const sendButton = $('#sendMessage');
    const closeButton = $('#closeChatbox');
    
    let financialData = null;

    // Show/hide chat toggle button based on form submission
    function updateChatVisibility() {
        if (financialData) {
            chatToggle.show();
        }
    }

    // Toggle chatbox
    chatToggle.click(function() {
        chatbox.show();
        chatToggle.hide();
        chatMessages.scrollTop(chatMessages[0].scrollHeight);
    });

    closeButton.click(function() {
        chatbox.hide();
        chatToggle.show();
    });

    // Send message
    function sendMessage() {
        const message = chatInput.val().trim();
        if (message) {
            // Add user message to chat
            appendMessage('user', message);
            chatInput.val('');

            // Send to server
            $.ajax({
                url: '/chat',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    message: message,
                    financialData: financialData
                }),
                success: function(response) {
                    if (response.success) {
                        appendMessage('assistant', response.response);
                    } else {
                        appendMessage('assistant', 'I apologize, but I encountered an error. Please try again.');
                    }
                },
                error: function() {
                    appendMessage('assistant', 'Sorry, I\'m having trouble connecting. Please try again later.');
                }
            });
        }
    }

    // Append message to chat
    function appendMessage(role, content) {
        const messageDiv = $('<div></div>')
            .addClass('message')
            .addClass(role === 'user' ? 'user-message' : 'assistant-message')
            .text(content);
        
        chatMessages.append(messageDiv);
        chatMessages.scrollTop(chatMessages[0].scrollHeight);
    }

    // Event listeners
    sendButton.click(sendMessage);
    chatInput.keypress(function(e) {
        if (e.which === 13) {
            sendMessage();
        }
    });

    // Update chat when financial data is submitted
    $('#financialForm').on('submit', function(e) {
        e.preventDefault();
        
        const children = [];
        $('.child-age').each(function(i) {
            children.push({
                age: parseInt($(this).val()),
                education_goal: $('.child-goal').eq(i).val()
            });
        });
        
        financialData = {
            age: parseInt($('#age').val()),
            current_savings: parseFloat($('#current_savings').val()),
            annual_income: parseFloat($('#annual_income').val()),
            retirement_age: parseInt($('#retirement_age').val()),
            children: children
        };

        // Show chat toggle after form submission
        updateChatVisibility();
        
        // Continue with existing form submission code...
    });
});