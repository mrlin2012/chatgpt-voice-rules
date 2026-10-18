# ChatGPT Voice IP rules for Mihomo / OpenClash

This repository downloads OpenAI's official ChatGPT Voice IP list and publishes:
- `voice.txt`: extracted CIDR networks.
- `voice.mrs`: compiled Mihomo binary IP-CIDR rule set.

GitHub Actions is configured to run daily at 07:17 China Standard Time and can be started manually from the **Actions** tab.

## OpenClash / Mihomo configuration

Add under `rule-providers:`:

```yaml
  chatgpt_voice:
    type: http
    behavior: ipcidr
    format: mrs
    url: "https://raw.githubusercontent.com/mrlin2012/chatgpt-voice-rules/main/voice.mrs"
    path: ./ruleset/chatgpt_voice.mrs
    interval: 86400
    # If the router cannot fetch GitHub directly, uncomment and set your proxy group:
    # proxy: "YOUR_PROXY_GROUP"
```

Add under `rules:` before broad/general routing rules:

```yaml
  - RULE-SET,chatgpt_voice,YOUR_PROXY_GROUP,no-resolve
```

Replace `YOUR_PROXY_GROUP` with your actual proxy group name. Remove your old manually maintained ChatGPT Voice IP-CIDR entries to avoid duplicate rules.

## Sources

- Official OpenAI Voice IP list: https://openai.com/chatgpt-voice.json
- OpenAI network recommendations: https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps

The repository publishes the rules subscription; it does not automatically edit your router configuration.
