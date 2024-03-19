<template>
  <div class="row" style="width: 100%; margin: auto;">
    <div class="nes-container with-title">
      <p style="color: #209cee;" class="title">{{ label }}</p>
      <div style="display: flex; width: 100%">

        <input class="form-control input-field" :class="{ 'underline': submitReady}" :id="'exampleDataList' + index" 
        placeholder="User to search..." v-model="searchQuery" 
        @input="searchUsers" @change="selectUser" style="width:70%">
        <div class="nes-select select-field"  style=" width:20%;">
          <select class="default-select selecti" v-model="selectedUser" :id="'datalistOptions' + index" @change="selectUser">
            <option value="" selected disabled>Select an User</option>
            <option v-for="result in searchResults" :value="result.name" :key="result.id">{{ result.name }}</option>
          </select>
        </div>
        <div v-if="noUserFound" class="object-fit-contain tooltip1" style="width: 10%">!
          <span class="tooltiptext1">No user named <span style="color:red; font-style: italic;">{{ this.searchQuery }}</span> found</span>
        </div>
        <div v-else-if="submitReady" style="position: relative; display: inline-block; margin: -7px auto auto auto; color: #99e857; font-size: 220%; font-weight: 900; transform: rotate(310deg)">
          L
        </div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  props: ['index', 'label'],
  data() {
    return {
      searchQuery: '',
      searchResults: [],
      selectedUser: null,
      showResults: true,
      noUserFound: false,
      error: '',
      submitReady: false,
    };
  },
  methods: {
    async searchUsers() {
      this.submitReady = false;
      if (this.searchQuery.trim() === '') {
        this.noUserFound = false;
      }
      
      try {
        if (this.searchQuery === "") {
          this.noUserFound = false;
          return;
        }
        const response = await fetch(`/endpoint/user/search/?search=${this.searchQuery}`);
        if (response.ok) {
          const data = await response.json();
          if (data == 0) {
            this.noUserFound = true;
            return;
          }
          this.noUserFound = false;
          this.searchResults = data;
        } else {
          console.error('Error searching users:', response.statusText);
        }
      } catch (error) {
        console.error('Error searching users:', error);
      }
    },

    selectUser(event) {
      const selectedResult = this.searchResults.find(result => result.name === event.target.value);
      if (selectedResult) {
        this.noUserFound = false;
        this.selectedUser = selectedResult;
        this.searchQuery = this.selectedUser.name
        this.submitReady = true;
        this.$emit('user-selected', this.selectedUser.name, this.index)

      }
    },
  },
};
</script>

<style>

.tooltip1 {
  position: relative;
  display: inline-block;
  color: red;
  font-size: 200%;
  font-weight: 900;
}

.tooltip1 .tooltiptext1 {
  visibility: hidden;
  background-color: black;
  border-radius: 6px;
  padding: 5px 5px;
  font-weight: normal;
  font-size: 1rem;
  white-space: nowrap;
  /* Position the tooltip */
  position: absolute;
  right: 100%;
  z-index: 100;
}

.tooltip1:hover .tooltiptext1 {
  visibility: visible;
}

.select-field select {
  border: none;
  color: transparent;
  border-image-slice: 0;
  background-color: transparent;
  margin: 0;
}

option {
  font-size: 1.3rem;
}

.selecti:focus-visible select {
  border:none;
  outline: none;
  background-color: transparent;
  box-shadow: none;
}

.input-field:focus {
  outline:none;
}

.input-field {
 border:none;
 width: 80%;
}

.underline {
  color: black;
  background-color: #f2f2f2;
  font-style: italic;
}

.select-field:hover{
    top: -3px
  }

</style>
