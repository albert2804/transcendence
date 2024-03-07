<template>
  <div class="row">
    <div class="search-container">
      <input class="form-control" :id="'exampleDataList' + index" 
             placeholder="User to search..." v-model="searchQuery" 
             @input="searchUsers" @change="selectUser" style="min-width: 200px;">
      <div v-if="noUserFound" class="object-fit-contain col-2 tooltip1">!
        <span class="tooltiptext1">No user named <span style="color:red; font-style: italic;">{{ this.searchQuery }}</span> found</span>
      </div>
      <select v-if="showResults" v-model="selectedUser" :id="'datalistOptions' + index" @change="selectUser">
        <option v-for="result in searchResults" :value="result.name" :key="result.id">{{ result.name }}</option>
      </select>
    </div>
  </div>
</template>


<script>
export default {
  props: ['index'],
  data() {
    return {
      searchQuery: '',
      searchResults: [],
      selectedUser: null,
      showResults: true,
      noUserFound: false,
      error: '',
    };
  },
  methods: {
    async searchUsers() {
      if (this.searchQuery.trim() === '') {
        this.showResults = true;
        this.noUserFound = false;
        // console.log("hi")
      }
      
      try {
        if (this.searchQuery === "") {
          this.noUserFound = false;
          this.showResults = true;
          return;
        }
        const response = await fetch(`/endpoint/user/search/?search=${this.searchQuery}`);
        if (response.ok) {
          const data = await response.json();
          if (data == 0) {
            this.noUserFound = true;
            return;
          }
          // console.log(data)
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
        // console.log(this.selectedUser)
        // console.log(this.index)
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
  font-size: 150%;
  font-weight: 900;
}

.tooltip1 .tooltiptext1 {
  visibility: hidden;
  background-color: black;
  color: #fff;
  border-radius: 6px;
  padding: 5px 5px;
  font-weight: normal;
  font-size: 70%;
  white-space: nowrap;
  /* Position the tooltip */
  position: absolute;
  right: 100%;
  z-index: 100;
}

.tooltip1:hover .tooltiptext1 {
  visibility: visible;
}

.search-container {
    display: flex;
    align-items: center;
  }

.search-container select {
  margin-left: 10px;
  height: 100%;
  width: 150px;
}

</style>
