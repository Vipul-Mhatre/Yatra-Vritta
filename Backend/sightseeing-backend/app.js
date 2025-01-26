const API_URL = "http://localhost:5000";

async function authenticate() {
    try {
        const response = await fetch(`${API_URL}/authenticate`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({})
        });
        const data = await response.json();
        document.getElementById("authResult").textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        document.getElementById("authResult").textContent = `Error: ${error.message}`;
    }
}

async function fetchCountryList() {
    const token = document.getElementById("countryToken").value;
    try {
        const response = await fetch(`${API_URL}/country-list`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ TokenId: token })
        });
        const data = await response.json();
        document.getElementById("countryResult").textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        document.getElementById("countryResult").textContent = `Error: ${error.message}`;
    }
}

async function fetchDestinationSearch() {
    const token = document.getElementById("destinationToken").value;
    const searchType = document.getElementById("searchType").value;
    const countryCode = document.getElementById("countryCode").value;
    try {
        const response = await fetch(`${API_URL}/destination-search`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ TokenId: token, SearchType: searchType, CountryCode: countryCode })
        });
        const data = await response.json();
        document.getElementById("destinationResult").textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        document.getElementById("destinationResult").textContent = `Error: ${error.message}`;
    }
}

async function fetchAgencyBalance() {
    const token = document.getElementById("agencyToken").value;
    const agencyId = document.getElementById("agencyId").value;
    const memberId = document.getElementById("memberId").value;
    try {
        const response = await fetch(`${API_URL}/agency-balance`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ TokenId: token, TokenAgencyId: agencyId, TokenMemberId: memberId })
        });
        const data = await response.json();
        document.getElementById("balanceResult").textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        document.getElementById("balanceResult").textContent = `Error: ${error.message}`;
    }
}