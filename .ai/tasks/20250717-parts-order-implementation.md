# Implementation Plan: Parts Order Mechanism

> **Objective:** Implement the full-stack functionality for buyers to create and submit requests for auto parts.
>
> **Architecture Document:** [004.6-parts-order-arch-en.md](../../docs/004-Architecture/004.6-parts-order-arch-en.md)
>
> **Last Updated:** 2025-07-17

## Phase 1: Backend - Data Models & Handbooks

- [ ] Create new Django app: `orders`.
- [ ] Create new Django app: `handbooks`.
- [ ] Add `orders` and `handbooks` to `INSTALLED_APPS` in settings.
- [ ] Implement `BuyerOrder`, `Vehicle`, `PartRequest`, `PartImage` models in the `orders` app.
- [ ] Implement `CarMake`, `CarModel`, `PartGroup` models in the `handbooks` app.
- [ ] Configure `django-modeltranslation` for localizable fields in handbook models.
- [ ] Create initial database migrations for both apps.
- [ ] Develop a management command to import `CarMake` and `CarModel` data from a CSV file.
- [ ] Develop a management command to import `PartGroup` data.
- [ ] Add models to the Django admin for basic CRUD operations.

## Phase 2: Backend - Business Logic & API

- [ ] Create Django `forms.ModelForm` for `Vehicle` and `PartRequest`.
- [ ] Implement a view function to display the main "Create Order" page.
- [ ] Implement a view that handles the form submission, creating `BuyerOrder`, `Vehicle`, and associated `PartRequest` objects in a single transaction.
- [ ] Implement logic to handle multiple `PartRequest` forms within a single `BuyerOrder` submission (e.g., using formsets).
- [ ] Implement image upload and handling for `PartImage`.
- [ ] Create an API endpoint (for HTMX) to provide autocomplete suggestions for the part `name` field based on handbook data.

## Phase 3: Frontend - UI/UX

- [ ] Create a new template `orders/create_order.html`.
- [ ] Build the main form structure using HTML and Tailwind CSS.
- [ ] Implement the "Part Details" section, including fields for name, group, origin, condition, etc.
- [ ] Use HTMX to fetch autocomplete suggestions for the part name as the user types.
- [ ] Implement a mechanism to dynamically add/remove up to 5 "Part Request" forms on the page using JavaScript (Alpine.js) and HTMX.
- [ ] Implement the "Vehicle Details" section of the form.
- [ ] Ensure the form is responsive and works well on mobile devices.
- [ ] Style validation errors returned from the server.

## Phase 4: Testing & Refinement

- [ ] Write unit tests for the `orders` and `handbooks` models.
- [ ] Write unit tests for the form validation and business logic in the views.
- [ ] Write integration tests for the entire order creation flow (from GET request to successful POST).
- [ ] Manually test the user flow on different browsers and devices.
- [ ] Review and refine the UI/UX based on testing feedback.
