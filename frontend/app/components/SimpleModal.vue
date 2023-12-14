<!-- 
  Simple modal component that can be used to display html content.
  modalTitle, modalId and ariaLabel are Strings.
  content is a String containing html.

  Example:
  <SimpleModal :content="modalContent" :modalTitle="'Response from Django API:'" modalId="exampleModal" ariaLabel="exampleModalLabel" />

  show the modal with:
  new bootstrap.Modal(document.getElementById('exampleModal')).show();
-->

<template>
    <div class="modal fade" :id="modalId" tabindex="-1" :aria-labelledby="ariaLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ modalTitle }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body" v-if="content" v-html="content"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'SimpleModal',
    props: {
      content: String, // html string
      modalTitle: String,
      modalId: String,
      ariaLabel: String,
    },
  };
  </script>

<!-- 
  used bootstrap components:
  https://getbootstrap.com/docs/5.3/components/modal/
 -->

