# Overview

This is a Ukrainian Telegram bot that receives screenshot photos from users, responds with thanks in Ukrainian, and forwards the images to a designated chat or channel. The bot runs 24/7 on Replit using a keep-alive mechanism and is designed to handle photo messages while encouraging users to send screenshots for other message types.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Bot Framework
- **aiogram**: Asynchronous Python Telegram Bot API framework chosen for its modern async/await support and clean API design
- **Polling-based**: Uses long polling instead of webhooks for simplicity in Replit environment

## Message Processing
- **Photo Handler**: Dedicated handler for photo content types that processes incoming images
- **Response System**: Automatic Ukrainian language responses to acknowledge photo receipt
- **Message Forwarding**: Direct forwarding of received photos to a configured destination chat

## Configuration Management
- **Environment Variables**: Bot token and forward chat ID stored as Replit Secrets for security
- **Error Handling**: Comprehensive validation of required environment variables at startup
- **Type Conversion**: Automatic conversion of chat ID from string to integer with error handling

## Keep-Alive Service
- **Flask Web Server**: Lightweight HTTP server running on port 5000 to prevent Replit from sleeping
- **Status Page**: HTML status page with Ukrainian styling to monitor bot health
- **Threading**: Keep-alive server runs in separate thread from main bot process

## Error Handling
- **Logging System**: Structured logging with timestamps and severity levels
- **Network Resilience**: Built-in handling for Telegram API errors and network issues
- **Graceful Degradation**: Bot continues operating even if individual message processing fails

## Deployment Strategy
- **Replit Native**: Designed specifically for Replit's execution environment
- **24/7 Operation**: Keep-alive mechanism ensures continuous operation
- **Single File Architecture**: Minimal file structure for easy maintenance and deployment

# External Dependencies

## Telegram Bot API
- **Primary Interface**: Official Telegram Bot API for all bot interactions
- **Message Types**: Handles photo messages and text responses
- **Chat Operations**: Forward messages between different chats/channels

## Replit Platform
- **Hosting Environment**: Runs on Replit's cloud infrastructure
- **Secrets Management**: Uses Replit Secrets for secure credential storage
- **Always-On Service**: Leverages Replit's execution model with keep-alive mechanism

## Python Libraries
- **aiogram**: Modern async Telegram Bot API framework
- **Flask**: Lightweight web framework for keep-alive server
- **asyncio**: Built-in async/await support for concurrent operations
- **logging**: Standard Python logging for monitoring and debugging

## Configuration Requirements
- **TELEGRAM_BOT_TOKEN**: Bot authentication token from BotFather
- **FORWARD_CHAT_ID**: Target chat/channel ID for photo forwarding