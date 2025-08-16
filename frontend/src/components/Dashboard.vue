<template>
  <div class="dashboard">
    <header class="header">
      <h1>UniFi SMS Gateway Dashboard</h1>
      <div class="user-info">
        <span>{{ user.email }}</span>
        <button @click="$emit('logout')" class="logout-btn">Logout</button>
      </div>
    </header>

    <div class="dashboard-grid">
      <!-- Device Status -->
      <div class="card">
        <h3>Device Status</h3>
        <button @click="checkDeviceStatus" :disabled="loadingStatus" class="refresh-btn">
          {{ loadingStatus ? 'Checking...' : 'Check Status' }}
        </button>
        <div v-if="deviceStatus" class="status-info">
          <pre>{{ deviceStatus }}</pre>
        </div>
      </div>

      <!-- Send SMS -->
      <div class="card">
        <h3>Send SMS</h3>
        <form @submit.prevent="sendSMS">
          <div class="form-group">
            <label for="toNumber">To Number:</label>
            <input 
              type="tel" 
              id="toNumber" 
              v-model="smsForm.toNumber" 
              required 
              placeholder="+1234567890"
            >
          </div>
          
          <div class="form-group">
            <label for="message">Message:</label>
            <textarea 
              id="message" 
              v-model="smsForm.message" 
              required 
              rows="3"
              placeholder="Enter your message..."
            ></textarea>
          </div>
          
          <button type="submit" :disabled="sendingSMS" class="send-btn">
            {{ sendingSMS ? 'Sending...' : 'Send SMS' }}
          </button>
        </form>
        
        <div v-if="smsResult" class="sms-result" :class="{ success: smsResult.success, error: !smsResult.success }">
          {{ smsResult.message }}
        </div>
      </div>

      <!-- SMS History -->
      <div class="card full-width">
        <h3>SMS History</h3>
        <button @click="loadSMSHistory" :disabled="loadingHistory" class="refresh-btn">
          {{ loadingHistory ? 'Loading...' : 'Refresh History' }}
        </button>
        
        <div v-if="smsHistory.length > 0" class="history-table">
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>To Number</th>
                <th>Message</th>
                <th>Status</th>
                <th>Direction</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="sms in smsHistory" :key="sms.id">
                <td>{{ formatDate(sms.timestamp) }}</td>
                <td>{{ sms.to_number }}</td>
                <td class="message-cell">{{ sms.message }}</td>
                <td>
                  <span class="status-badge" :class="sms.status">
                    {{ sms.status }}
                  </span>
                </td>
                <td>{{ sms.direction }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div v-else-if="!loadingHistory" class="no-data">
          No SMS history found.
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Dashboard',
  props: {
    user: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      deviceStatus: '',
      loadingStatus: false,
      smsForm: {
        toNumber: '',
        message: ''
      },
      sendingSMS: false,
      smsResult: null,
      smsHistory: [],
      loadingHistory: false
    }
  },
  mounted() {
    this.loadSMSHistory()
  },
  methods: {
    async checkDeviceStatus() {
      this.loadingStatus = true
      try {
        const token = localStorage.getItem('token')
        const response = await axios.get('/api/sms/status', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        
        const data = response.data
        this.deviceStatus = `DEVICE INFO:\n${data.device_info}\n\nSIM INFO:\n${data.sim_info}\n\nTEMPERATURE INFO:\n${data.temperature_info}`
      } catch (error) {
        this.deviceStatus = `Error: ${error.response?.data?.error || error.message}`
      } finally {
        this.loadingStatus = false
      }
    },

    async sendSMS() {
      this.sendingSMS = true
      this.smsResult = null
      
      try {
        const token = localStorage.getItem('token')
        const response = await axios.post('/api/sms/send', {
          to_number: this.smsForm.toNumber,
          message: this.smsForm.message
        }, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        
        this.smsResult = {
          success: response.data.success,
          message: response.data.success ? 'SMS sent successfully!' : response.data.message
        }
        
        if (response.data.success) {
          this.smsForm.toNumber = ''
          this.smsForm.message = ''
          this.loadSMSHistory() // Refresh history
        }
      } catch (error) {
        this.smsResult = {
          success: false,
          message: error.response?.data?.error || 'Failed to send SMS'
        }
      } finally {
        this.sendingSMS = false
      }
    },

    async loadSMSHistory() {
      this.loadingHistory = true
      try {
        const token = localStorage.getItem('token')
        const response = await axios.get('/api/sms/history', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        
        this.smsHistory = response.data
      } catch (error) {
        console.error('Failed to load SMS history:', error)
      } finally {
        this.loadingHistory = false
      }
    },

    formatDate(timestamp) {
      return new Date(timestamp).toLocaleString()
    }
  }
}
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 1rem 2rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.header h1 {
  color: #333;
  margin: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logout-btn {
  padding: 0.5rem 1rem;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
}

.logout-btn:hover {
  background: #c82333;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card.full-width {
  grid-column: 1 / -1;
}

.card h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #333;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: 500;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

.refresh-btn,
.send-btn {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  margin-bottom: 1rem;
}

.refresh-btn:hover,
.send-btn:hover {
  transform: translateY(-1px);
}

.refresh-btn:disabled,
.send-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.status-info {
  background: #f8f9fa;
  border-radius: 6px;
  padding: 1rem;
  overflow-x: auto;
}

.status-info pre {
  margin: 0;
  white-space: pre-wrap;
  font-size: 0.9rem;
}

.sms-result {
  margin-top: 1rem;
  padding: 0.75rem;
  border-radius: 6px;
  text-align: center;
}

.sms-result.success {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.sms-result.error {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.history-table {
  overflow-x: auto;
}

.history-table table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.history-table th,
.history-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.history-table th {
  background: #f8f9fa;
  font-weight: 600;
}

.message-cell {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
  text-transform: uppercase;
}

.status-badge.sent {
  background: #d4edda;
  color: #155724;
}

.status-badge.pending {
  background: #fff3cd;
  color: #856404;
}

.status-badge.failed {
  background: #f8d7da;
  color: #721c24;
}

.no-data {
  text-align: center;
  color: #666;
  font-style: italic;
  margin-top: 1rem;
}
</style>
