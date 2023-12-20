import React from 'react'

export default function MessageAlert({ messages }) {
    return (
        <div className="scrolling-message-container">
          {messages.map((message, index) => (
            <div key={index} className="scrolling-message-item">
              {message}
            </div>
          ))}
        </div>
    );
};


