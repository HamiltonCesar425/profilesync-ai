import { useEffect } from "react";

import type { Technology, TechnologyCreate } from "../../types/technology";

import { TechnologyForm } from "./TechnologyForm";

interface TechnologyModalProps {
  isOpen: boolean;
  technology?: Technology | null;
  isSubmitting: boolean;
  onSubmit: (data: TechnologyCreate) => Promise<void>;
  onClose: () => void;
}

export function TechnologyModal({
  isOpen,
  technology,
  isSubmitting,
  onSubmit,
  onClose,
}: TechnologyModalProps) {
  useEffect(() => {
    if (!isOpen) {
      return;
    }

    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape" && !isSubmitting) {
        onClose();
      }
    }

    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [isOpen, isSubmitting, onClose]);

  useEffect(() => {
    if (!isOpen) {
      return;
    }

    const originalOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    return () => {
      document.body.style.overflow = originalOverflow;
    };
  }, [isOpen]);

  if (!isOpen) {
    return null;
  }

  const modalTitle = technology ? "Editar tecnologia" : "Cadastrar tecnologia";

  function handleBackdropClick(event: React.MouseEvent<HTMLDivElement>) {
    if (event.target === event.currentTarget && !isSubmitting) {
      onClose();
    }
  }

  return (
    <div
      className="modal-backdrop"
      role="presentation"
      onMouseDown={handleBackdropClick}
    >
      <section
        className="modal-content technology-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="technology-modal-title"
      >
        <div className="modal-header">
          <h2 id="technology-modal-title">{modalTitle}</h2>

          <button
            className="modal-close-button"
            type="button"
            aria-label="Fechar modal"
            onClick={onClose}
            disabled={isSubmitting}
          >
            ×
          </button>
        </div>

        <TechnologyForm
          technology={technology}
          isSubmitting={isSubmitting}
          onSubmit={onSubmit}
          onCancel={onClose}
        />
      </section>
    </div>
  );
}
