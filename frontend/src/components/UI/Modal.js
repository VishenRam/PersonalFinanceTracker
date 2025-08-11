import React from 'react';

const Modal = ({ children, onClose }) => {
    return (
        <div className="modal" onClick={onClose}>
            <div className='modal-content' onClick={(e) => e.stopPropagation()}>
                <span className="close-btn" onClick={onClose}>&times;</span>
                {children}
            </div>
        </div>
    );
};

export default Modal;