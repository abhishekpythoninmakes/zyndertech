// Custom admin JavaScript for Zynder Tech

document.addEventListener("DOMContentLoaded", () => {
  // Enhanced image preview functionality
  const imageFields = document.querySelectorAll(".field-image_preview img, .field-logo_preview img")
  imageFields.forEach((img) => {
    img.addEventListener("click", function () {
      // Create modal for full-size image preview
      const modal = document.createElement("div")
      modal.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.8);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 9999;
                cursor: pointer;
            `

      const fullImg = document.createElement("img")
      fullImg.src = this.src
      fullImg.style.cssText = `
                max-width: 90%;
                max-height: 90%;
                border-radius: 8px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            `

      modal.appendChild(fullImg)
      document.body.appendChild(modal)

      modal.addEventListener("click", () => {
        document.body.removeChild(modal)
      })
    })
  })

  // Auto-save functionality for forms
  const forms = document.querySelectorAll("form")
  forms.forEach((form) => {
    const inputs = form.querySelectorAll("input, textarea, select")
    inputs.forEach((input) => {
      input.addEventListener("change", () => {
        // Add visual feedback for unsaved changes
        if (!form.classList.contains("has-changes")) {
          form.classList.add("has-changes")
          const saveButton = form.querySelector('input[type="submit"]')
          if (saveButton) {
            saveButton.style.background = "linear-gradient(135deg, #ef4444, #dc2626)"
            saveButton.value = "Save Changes *"
          }
        }
      })
    })
  })

  // Enhanced search functionality
  const searchInputs = document.querySelectorAll('input[name="q"]')
  searchInputs.forEach((input) => {
    input.addEventListener("input", function () {
      const query = this.value.trim()
      if (query.length > 2) {
        // Add loading state
        this.style.background =
          'url("data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHZpZXdCb3g9IjAgMCAyMCAyMCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEwIDNWN0wxNCA1TDEwIDNaIiBmaWxsPSIjOTk5Ii8+CjxhbmltYXRlVHJhbnNmb3JtIGF0dHJpYnV0ZU5hbWU9InRyYW5zZm9ybSIgdHlwZT0icm90YXRlIiB2YWx1ZXM9IjAgMTAgMTA7MzYwIDEwIDEwIiBkdXI9IjFzIiByZXBlYXRDb3VudD0iaW5kZWZpbml0ZSIvPgo8L3N2Zz4=") no-repeat right 10px center'
      }
    })
  })

  // Bulk action confirmations
  const actionSelect = document.querySelector('select[name="action"]')
  const actionButton = document.querySelector('button[title="Run the selected action"]')

  if (actionSelect && actionButton) {
    actionButton.addEventListener("click", (e) => {
      const selectedAction = actionSelect.value
      const checkedItems = document.querySelectorAll('input[name="_selected_action"]:checked')

      if (checkedItems.length === 0) {
        e.preventDefault()
        alert("Please select at least one item.")
        return
      }

      if (selectedAction.includes("delete") || selectedAction.includes("inactive")) {
        const confirmMessage = `Are you sure you want to ${selectedAction.replace("_", " ")} ${checkedItems.length} item(s)?`
        if (!confirm(confirmMessage)) {
          e.preventDefault()
        }
      }
    })
  }

  // Real-time validation
  const emailInputs = document.querySelectorAll('input[type="email"]')
  emailInputs.forEach((input) => {
    input.addEventListener("blur", function () {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (this.value && !emailRegex.test(this.value)) {
        this.style.borderColor = "#ef4444"
        this.style.boxShadow = "0 0 0 3px rgba(239, 68, 68, 0.1)"
      } else {
        this.style.borderColor = "#10b981"
        this.style.boxShadow = "0 0 0 3px rgba(16, 185, 129, 0.1)"
      }
    })
  })

  // Phone number formatting
  const phoneInputs = document.querySelectorAll('input[name*="phone"]')
  phoneInputs.forEach((input) => {
    input.addEventListener("input", function () {
      // Remove non-numeric characters except + and spaces
      this.value = this.value.replace(/[^\d+\s-()]/g, "")
    })
  })
})

// Email configuration test function
function testEmailConnection(configId) {
  const button = event.target
  const originalText = button.innerHTML

  button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Testing...'
  button.style.pointerEvents = "none"

  // Simulate email test (replace with actual AJAX call)
  setTimeout(() => {
    button.innerHTML = '<i class="fas fa-check"></i> Success'
    button.style.color = "#10b981"

    setTimeout(() => {
      button.innerHTML = originalText
      button.style.color = ""
      button.style.pointerEvents = ""
    }, 2000)
  }, 2000)
}

// Dashboard statistics
function loadDashboardStats() {
  // Add dashboard statistics widgets
  const dashboard = document.querySelector(".dashboard")
  if (dashboard) {
    const statsWidget = document.createElement("div")
    statsWidget.className = "module"
    statsWidget.innerHTML = `
            <h2>Quick Stats</h2>
            <div class="stats-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; padding: 15px;">
                <div class="stat-item" style="text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px;">
                    <div style="font-size: 24px; font-weight: bold; color: #f59e0b;">0</div>
                    <div style="font-size: 12px; color: #666;">Active Services</div>
                </div>
                <div class="stat-item" style="text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px;">
                    <div style="font-size: 24px; font-weight: bold; color: #10b981;">0</div>
                    <div style="font-size: 12px; color: #666;">Training Programs</div>
                </div>
                <div class="stat-item" style="text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px;">
                    <div style="font-size: 24px; font-weight: bold; color: #ef4444;">0</div>
                    <div style="font-size: 12px; color: #666;">Pending Inquiries</div>
                </div>
                <div class="stat-item" style="text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px;">
                    <div style="font-size: 24px; font-weight: bold; color: #8b5cf6;">0</div>
                    <div style="font-size: 12px; color: #666;">Testimonials</div>
                </div>
            </div>
        `
    dashboard.insertBefore(statsWidget, dashboard.firstChild)
  }
}

// Initialize dashboard on load
if (window.location.pathname === "/admin/") {
  loadDashboardStats()
}
