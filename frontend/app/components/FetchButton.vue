<!--
  This Button is used to fetch data from an endpoint and emit it to the parent component/page.
  The parent component/page should have a method to process the data. (@data-received="methodToProcessData")

  Example:
        <FetchButton :fetchUrl="'/endpoint/anyUrl'" :showErrModal=false @data-received="methodToProcessData">Click me!</FetchButton>

  If you want to show an error modal when the fetch fails, set showErrModal to true.
-->

<template>
  <div>
    
    <div>
      <button type="button" class="btn btn-primary" @click="fetchData">
        <slot>Click me!</slot>
      </button>
    </div>
    <SimpleModal v-show="errormsg" :content="errormsg" :modalTitle="'Fetch-Error:'" modalId="fetchErrModal" ariaLabel="fetchErrModalLabel" />
  </div>
</template>

<script>
export default {
  name: 'FetchButton',
  props: {
    fetchUrl: String,
    showErrModal: {
      type: Boolean,
      default: false,
    }
  },
  emits: ['data-received'],
  data() {
    return {
      errormsg: null,
    };
  },
  methods: {
    fetchData() {
      fetch(this.fetchUrl)
        .then((response) => {
          if (!response.ok) {
            // check for error (and open error modal if showErrModal is true)
            this.errormsg = 'Error: ' + response.status + ' ' + response.statusText;
            if (this.showErrModal) {
              this.$nextTick(() => {
                new bootstrap.Modal(document.getElementById('fetchErrModal')).show();
              });
            }
            throw new Error(this.errormsg);
          }
          // check the response type and return the data in the correct format
          const contentType = response.headers.get('content-type');
          if (contentType.includes('application/json')) {
            return response.json();
          } else if (contentType.includes('text/html') || contentType.includes('text/plain')) {
            return response.text();
          }
          // do we need this uncommented types?
          // else if (contentType.includes('multipart/form-data')) {
          //   return response.formData();
          // } else if (contentType.includes('application/octet-stream')) {
          //   return response.arrayBuffer();
          // }
          else {
            return response.text();
          }
        })
        .then((data) => {
          this.$emit('data-received', data);
        })
        .catch((error) => {
          console.error('FetchButton:', error);
        });
    },
  },
};
</script>

<!--
  used bootstrap components:
  https://getbootstrap.com/docs/5.3/components/buttons/
  https://getbootstrap.com/docs/5.3/components/modal/ (inside SimpleModal.vue)
-->
  